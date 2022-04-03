from django.urls import path
from . import views


urlpatterns = [
        path('food/', views.FoodList.as_view()),
        path('food/<int:pk>/', views.FoodDetail.as_view()),
        path('users/', views.UserList.as_view()),
        path('users/<int:pk>/', views.UserDetail.as_view()),
        path('users/register/', views.UserCreate.as_view()),
        path('users/change_password/<int:pk>/', views.UserChangePassword.as_view()),
        path('calorie_count/<str:usr>/<int:pk>/', views.Counting.as_view()),
]


