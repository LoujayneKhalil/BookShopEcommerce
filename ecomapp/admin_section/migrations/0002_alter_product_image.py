# Generated by Django 4.2.4 on 2023-09-11 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_section', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
