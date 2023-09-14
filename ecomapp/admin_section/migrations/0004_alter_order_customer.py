# Generated by Django 4.2.4 on 2023-09-14 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_section', '0001_initial'),
        ('admin_section', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_section.customer'),
        ),
    ]
