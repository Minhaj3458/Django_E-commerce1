# Generated by Django 3.2.3 on 2021-09-09 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='category/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='EcommerceApp.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=15, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_name', models.CharField(max_length=200)),
                ('preview_des', models.CharField(max_length=255, verbose_name='Short Descriptions')),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='product/')),
                ('new_price', models.FloatField()),
                ('old_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('is_stock', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catagory', to='EcommerceApp.category')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
