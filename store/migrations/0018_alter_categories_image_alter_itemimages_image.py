# Generated by Django 4.1 on 2022-10-14 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_items_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=models.ImageField(default='no-image.png', upload_to='category_covers', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='itemimages',
            name='image',
            field=models.ImageField(default='no-image.png', upload_to='', verbose_name='Изображение'),
        ),
    ]
