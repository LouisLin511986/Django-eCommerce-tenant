from django.db import models
from django.db.models import AutoField
from core.helpers import *
from django.utils.translation import get_language

class Product(models.Model):
    '''
    商品模型
    '''
    product_Number = models.AutoField(primary_key=True, unique=True, verbose_name="商品編號")
    name = models.CharField(verbose_name="商品名稱", null = False, blank = False, max_length = 50)
    description = models.TextField(verbose_name="商品介紹", null = False, blank = True, default = "暫無資料",  max_length = 500)
    price = models.DecimalField(verbose_name="價格",max_digits=5,decimal_places=0, null = False, blank = False)
    inventory = models.IntegerField(verbose_name="商品庫存量", null = False, blank = False, default = 0)
    created = models.DateTimeField(verbose_name="創建日期", auto_now_add = True)
    modified = models.DateTimeField(verbose_name="最後更新日期", auto_now = True)
    date_Published = models.DateTimeField(verbose_name="上架日期", auto_now = True)
    category = models.ForeignKey('products.ProductCategory', verbose_name="商品類別", blank=False, null=True, on_delete=models.RESTRICT, related_name="product_set")

    class Meta:
        verbose_name = ('商品')
        verbose_name_plural = ('商品')
        ordering = ['-product_Number']

    def __str__(self):
        return f'{self.name}'
    

class ProductCategory(models.Model):
    '''
    商品分類模型
    '''
    name = models.CharField(verbose_name="商品分類名稱", null = False, blank = False, max_length = 50)
    description = models.TextField(verbose_name="商品分類描述", null = False, blank = True, default = "暫無資料",  max_length = 500)
    created = models.DateTimeField(verbose_name="創建日期", auto_now_add = True)
    modified = models.DateTimeField(verbose_name="最後更新日期", auto_now = True)
    image = models.ImageField(verbose_name="圖片", null = True, blank = True, upload_to = upload_handle)

    class Meta:
        verbose_name = '商品分類'
        verbose_name_plural = '商品分類'
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'


class ProductImage(models.Model):
    name = models.CharField(verbose_name="圖片描述", null = False, blank = True, default = "暫無資料",  max_length = 500)
    product = models.ForeignKey('products.Product', verbose_name="商品", on_delete=models.CASCADE, related_name="product_image_set")
    image = models.ImageField(verbose_name="圖片", null = True, blank = True, upload_to = upload_handle)
    order = models.PositiveIntegerField(verbose_name="編號", null=True, blank=True)

    class Meta:
        verbose_name = '商品圖片'
        verbose_name_plural = '商品圖片'
        ordering = ['order']

    def __str__(self):
        return f'{self.name}'


class RelationalProduct(models.Model):
    product = models.ForeignKey('products.Product', verbose_name="商品名稱", on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', verbose_name="編號", on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name="數量", default=1)

    @property
    def name(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    def __str__(self):
        return ""