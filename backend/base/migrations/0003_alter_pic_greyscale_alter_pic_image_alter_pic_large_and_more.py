# Generated by Django 4.1.4 on 2022-12-31 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='greyscale',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pic',
            name='large',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pic',
            name='medium',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pic',
            name='thumb',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]