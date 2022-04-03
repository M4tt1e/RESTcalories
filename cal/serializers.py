from rest_framework import serializers
from .models import Macros, Food, Counter
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwordfields did not match'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'owner', 'email']
        extra_kwargs = {
                'id': {'read_only': True},
                'username': {'read_only': True},
        }


class MacrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Macros
        fields = ['protein', 'carbs', 'fat']



class FoodSerializer(serializers.ModelSerializer):
    macros = MacrosSerializer(required=True)    
    usr = serializers.ReadOnlyField(source='usr.username')
     
    def create(self, validated_data):
        macros_data = validated_data.pop('macros')
        macro = MacrosSerializer.create(MacrosSerializer(), validated_data=macros_data)
        food_item = Food.objects.create(macros=macro, **validated_data)
        return food_item
    
    def update(self, instance, validated_data):
        if validated_data.get('macros'):
            macros_data = validated_data.pop('macros')
            macro = instance.macros

            macro.protein = macros_data.get('protein', macro.protein)
            macro.carbs = macros_data.get('carbs', macro.carbs)
            macro.fat = macros_data.get('fat', macro.fat)
            macro.save()
        instance = super().update(instance, validated_data)
        return instance


    class Meta:
        model = Food
        fields = ['id', 'name', 'favorite', 'description', 'macros','calories', 'grams','created', 'usr']

        validators = [
                UniqueTogetherValidator(
                    queryset=Food.objects.all(),
                    fields =['name', 'calories']
                    )
                ]


class CounterSerializer(serializers.ModelSerializer):    
    calorie_count_owner = serializers.ReadOnlyField(source='usr.username')
    calories_count = serializers.IntegerField(source='calculated_calories')

    def validate(self, data):
        """
        Check if food object is owned by current user
        """
        if data['calorie_count_owner'] != data['total_foods_day']:
                raise serializers.ValidationError('Cannot use other`s food')
        return data

    class Meta:
        model = Counter
        fields = ['calorie_count_owner','total_foods_day', 'calories_count' ,'associated_date']
        extra_kwargs={
                'calories_count':{'read_only': True}
                }
#Can't set attribute error when trying to post data
#Only allow owners of food to use them in calorie counting somehowvalidate (validation incorrect)



