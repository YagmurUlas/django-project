# Generated by Django 3.0.3 on 2020-03-26 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20200326_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Trip')),
            ],
        ),
        migrations.CreateModel(
            name='ImageActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='activity',
            name='image',
        ),
        migrations.DeleteModel(
            name='Images',
        ),
        migrations.AddField(
            model_name='imageactivity',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Activity'),
        ),
    ]
