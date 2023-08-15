from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.db import models
from uuid import uuid4

from django.urls import reverse

from store.validators import validate_file_size

class ProductAvailableManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(inventory__gte=1)

class Collection(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True,null=True,blank=True)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('store:product_list_by_collection', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
                
    class Meta:
        ordering = ['title']
        indexes = [models.Index(fields=["title"])]
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')

    objects = models.Manager()
    available = ProductAvailableManager()

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']
        indexes = [models.Index(fields=["id","slug"]),
                   models.Index(fields=['title']),
                   models.Index(fields=["-last_update"])]
        


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='store/images',
        validators=[validate_file_size])



class Order(models.Model):
    class PaidStatus(models.TextChoices):
        PENDING = "PD" , 'Pending'
        SUCCESS = 'SC', 'Success'
        FAILED = 'FA', 'Failed'


    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    postal_code = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.CharField(max_length=2, choices= PaidStatus.choices, default=PaidStatus.PENDING)
    stripe_id = models.CharField(max_length=250, blank=True)
    class Meta:
        ordering = ['-created']
        indexes = [ models.Index(fields=['-created']), ]

    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_stripe_url(self):
        if not self.stripe_id: return ''
        if '_test_' in settings.STRIPE_SECRET_KEY: path = '/test/'
        else: path = '/'  # Stripe path for real payments      
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity

