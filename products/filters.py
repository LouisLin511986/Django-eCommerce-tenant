from django import forms
from .models import *
import django_filters

class ProductModelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '名稱...'})
    )

    class Meta:
        model = Product
        fields = '__all__'