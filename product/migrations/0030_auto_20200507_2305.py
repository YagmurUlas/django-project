# Generated by Django 3.0.3 on 2020-05-07 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20200426_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageactivity',
            name='activity',
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('Category', 'Category'), ('Activity', 'Activity')], default='Category', max_length=10),
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='ImageActivity',
        ),
    ]
