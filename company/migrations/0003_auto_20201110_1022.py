# Generated by Django 3.1.3 on 2020-11-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20201107_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image_url',
            field=models.URLField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='exploremaincategory',
            name='image_url',
            field=models.URLField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='exploresubcategory',
            name='image_url',
            field=models.URLField(max_length=2000),
        ),
    ]
