# Generated by Django 4.2 on 2023-05-30 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_localesetting_translatesetting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translatesetting',
            name='locale',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='language',
        ),
        migrations.AlterField(
            model_name='setting',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='LocaleSetting',
        ),
        migrations.DeleteModel(
            name='TranslateSetting',
        ),
    ]