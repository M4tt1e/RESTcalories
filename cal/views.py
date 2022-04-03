from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions


from django.contrib.auth.models import User


from .models import Food, Macros, Counter
from .permissions import IsOwner, IsUser
from .serializers import FoodSerializer, MacrosSerializer,CounterSerializer, UserSerializer, UserCreateSerializer, UserChangePasswordSerializer

class Counting(generics.RetrieveUpdateAPIView):
    serializer_class = CounterSerializer
    queryset = Counter.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(usr__username=self.kwargs['usr'])


class FoodList(generics.ListAPIView):#APIView): 
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get(self, request):
        food = Food.objects.filter(usr=self.request.user) #users see own only
        serializer = FoodSerializer(food, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usr=self.request.user) 
            #magic line because .save() alone can't work as I want to. 
            #logged in user will be autofilled in usr spot
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FoodDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_food(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'error': 'Food item does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def get(self, request,pk):
        food = self.get_food(pk)
        if food.usr == self.request.user:
            serializer = FoodSerializer(food)
            return Response(serializer.data)
        return Response({'error': 'You do not have permission to view this item'}, status=status.HTTP_403_FORBIDDEN)
        #if trying to access not your food via url 403 forbidden will appear


    def put(self, request, pk):
        food = self.get_food(pk)
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#error because of macros and name
    def patch(self, request, pk):
        food = self.get_food(pk)
        serializer = FoodSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        food = self.get_food(pk)
        food.delete()
        return Response({'deleted':'Your item was deleted'}, status=status.HTTP_204_NO_CONTENT)
  


class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

#isUser does not work properly. No user has access to patch
class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,IsUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

