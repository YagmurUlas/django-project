# Generated by Django 3.0.3 on 2020-05-14 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20200507_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Category', 'Category'), ('Activity', 'Activity')], default='Category', max_length=10),
        ),
    ]