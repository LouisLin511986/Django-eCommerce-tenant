# Generated by Django 4.2 on 2023-06-04 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('未付款', '未付款'), ('付款失敗', '付款失敗'), ('已付款，等待裝運', '已付款，等待裝運'), ('運輸中', '運輸中'), ('訂單完成', '訂單完成'), ('取消', '取消')], default='未付款', max_length=100, verbose_name='狀態'),
        ),
    ]
