from django.db import models
from django.contrib.auth.models import User
from user_section.models import Customer

import os


class Admin(models.Model):
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    hire_date = models.DateField()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


def get_image_upload_path(instance, filename):
    return os.path.join('product_images', str(instance.id), filename)


class Product(models.Model):
    name_en = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_upload_path)
    isbn = models.CharField(max_length=13, unique=True,
                            blank=True, null=True, verbose_name="ISBN-13")

    def __str__(self):
        return f"{self.name_en}"


class Order(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    def __str__(self):
        return f"Order {self.id}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_count = models.IntegerField()

    def __str__(self):
        return f"{self.order}"
