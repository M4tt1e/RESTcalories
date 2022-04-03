import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Food, Macros
from .serializers import FoodSerializer, MacrosSerializer, UserSerializer


