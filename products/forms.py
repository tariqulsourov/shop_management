from django import forms

from .models import Brand, ProductType, Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['p_type','brand','name','description','p_image','volume_weight',
                  'buying_price','available_quantity','bar_code','bar_code_image','selling_price']

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['type_name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']
        