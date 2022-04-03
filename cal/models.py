from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
from django.utils import timezone

class Macros(models.Model):
    protein = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField()
    fat = models.PositiveIntegerField()


    def __str__(self):
        return "p: " + str(self.protein)+"g" + " c: " + str(self.carbs)+"g" + " f: " + str(self.fat)+"g"

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    macros = models.OneToOneField(Macros, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    grams = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    created = models.DateField(auto_now_add=True)

    usr = models.ForeignKey('auth.User', related_name='owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Counter(models.Model):
    total_foods_day = models.ManyToManyField(Food)
    associated_date = models.DateField(auto_now_add = True)

    usr = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='calorie_count_owner')
    
    @property
    def calculated_calories(self):
        return sum(x.calories for x in self.total_foods_day.all())
    
    def eaten_today(self):
        self.associated_date >= timezone.now() - datetime.timedelta(days=1)

