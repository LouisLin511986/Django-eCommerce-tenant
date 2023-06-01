from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        widgets={
            'product_Number':forms.HiddenInput(),
            'name':forms.TextInput(attrs={'style': 'width:50%;', 'placeholder': '商品名稱'}),
            'description':forms.Textarea(attrs={'style': 'width:50%;', 'placeholder': '商品介紹'}),
            'price':forms.TextInput(attrs={'style': 'width:50%;', 'placeholder': '價格'}),
            'inventory':forms.IntegerField(attrs={'style': 'width:50%;', 'placeholder': '商品庫存量'}),
            'created':forms.HiddenInput(),
            'modified':forms.HiddenInput(),
            'date_Published':forms.HiddenInput(),
            'category':forms.HiddenInput(),
        }
        labels = {
            'name':'',
            'description':'',
            'price':'',
            'inventory':'',
        }