from django.forms import ModelForm
from django import forms
from accounts.models import Order, Customer


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'