from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Order(models.Model):
    '''
    訂單
    '''
    order_id = models.CharField(verbose_name = "訂單編號", db_index = True, max_length=20)
    email = models.EmailField(verbose_name = "電子信箱", max_length=255)
    product = models.ManyToManyField('products.Product', related_name='order_set', through='products.RelationalProduct')
    name = models.CharField(verbose_name = "聯絡人", max_length=50)
    phone = models.CharField(verbose_name = "電話", max_length=50 )
    district = models.CharField(verbose_name = "區", max_length=50)
    zipcode = models.CharField(verbose_name = "郵政編碼", max_length=50)
    address = models.CharField(verbose_name = "地址", max_length=255)
    total = models.PositiveIntegerField(verbose_name = "總金額", default=0)
    created = models.DateTimeField(verbose_name = "創建時間", auto_now_add=True)
    modified = models.DateTimeField(verbose_name = "最後修改時間", auto_now_add=True)
    status = models.CharField(
        _('狀態'), 
        max_length=100, 
        choices=(("未付款", _("未付款")), ("付款失敗", _("付款失敗")), ("已付款，等待裝運", _("已付款，等待裝運")), ("運輸中", _("運輸中")), ("訂單完成", _("訂單完成")), ("取消", _("取消"))), 
        default="未付款",
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            self.order_id = f'ORDER{self.id:08}'
            super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = '訂單'
        verbose_name_plural = '訂單'

    def __str__(self):
        return f'{self.order_id}'