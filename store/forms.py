from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User 
from django import forms
import django_filters

from store.models import Product

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields =['username','email', 'first_name', 'last_name','password1','password2'] 


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields= ['price']
