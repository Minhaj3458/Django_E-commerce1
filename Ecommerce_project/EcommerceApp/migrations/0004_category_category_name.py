# Generated by Django 3.2.3 on 2021-09-12 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcommerceApp', '0003_auto_20210909_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_Name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
