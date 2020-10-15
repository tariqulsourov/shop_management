from django.db import models

# Create your models here.

class Brand(models.Model):
    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.brand_name
    
    brand_name = models.CharField(max_length= 30, null=False, default='')


class ProductType(models.Model):
    class Meta:
        db_table = 'product_type'

    def __str__(self):
        return self.type_name
    
    type_name = models.CharField(max_length= 30, null=False, default='')


class Products(models.Model):
    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.id
    
    p_type = models.ForeignKey(ProductType, null=True, default=0, on_delete = models.SET_NULL)
    brand = models.ForeignKey(Brand, null=True, default=0, on_delete = models.SET_NULL)
    name = models.CharField(max_length= 30, null=False, default='')
    description = models.TextField(null=True, default='')
    p_image = models.ImageField(upload_to = 'static/files/products')
    volume_weight = models.CharField(max_length= 20, null=False, default='')
    buying_price = models.IntegerField(max_length= 5, null=False, default=0)
    available_quantity = models.IntegerField(max_length= 3, null=False, default=0)
    bar_code = models.CharField(max_length= 30, null=False, default='')
    bar_code_image = models.ImageField(upload_to = 'static/files/bar_codes')
    selling_price = models.IntegerField(max_length= 5, null=False, default=0)



    