from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


def generate_unique_slug(model, value, slug_field_name='slug'):
    base_slug = slugify(value)
    slug = base_slug
    index = 1
    lookup = {slug_field_name: slug}
    while model.objects.filter(**lookup).exists():
        index += 1
        slug = f"{base_slug}-{index}"
        lookup[slug_field_name] = slug
    return slug


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category')

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(Product, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ✅ THIS IS REQUIRED (Cart model)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()