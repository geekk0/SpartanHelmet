# Generated by Django 4.1 on 2022-08-11 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_item_itemimages_of_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=models.ImageField(default='no-image.png', upload_to='media/category_covers', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='itemimages',
            name='image',
            field=models.ImageField(default='no-image.png', upload_to='media', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='items',
            name='main_image',
            field=models.ImageField(default='no-image.png', upload_to='media/item_covers', verbose_name='Основное изображение'),
        ),
    ]
