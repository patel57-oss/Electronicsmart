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
    background_image = models.ImageField(upload_to='category/backgrounds', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='subcategory')
    background_image = models.ImageField(upload_to='subcategory/backgrounds', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(SubCategory, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


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
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Mark this product as featured")

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
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='delivered')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()


class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} stars by {self.user.username}"


class ContactFeedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.email})"

    class Meta:
        ordering = ['-created_at']

