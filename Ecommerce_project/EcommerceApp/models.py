from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    category_Name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(blank=True, upload_to='category/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_Name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'categories'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=False, blank=False)
    preview_des = models.CharField(max_length=255, verbose_name='Short Descriptions')
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='product/')
    new_price = models.FloatField()
    old_price = models.FloatField(default=0.00, blank=True, null=True)
    is_stock = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-created_at']
    def get_product_url(self):
        return reverse('EcommerceApp:product_details', kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        return super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.FileField(upload_to='pro_gallry')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.product_name)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.item}"
    def get_total (self):
        total = self.item.new_price * self.quantity
        float_total = format(total, '0.2f')
        return float_total

class Order(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   orderiteam = models.ManyToManyField(Cart)
   ordered = models.BooleanField(default=False)
   created = models.DateTimeField(auto_now_add=True)
   paymentId = models.CharField(max_length=255, blank=True, null=True)
   orderId = models.CharField(max_length=255, blank=True, null=True)

   def get_totals(self):
       total = 0
       for order_item in self.orderiteam.all():
           total += float(order_item.get_total())
       return total


class Variation_manager(models.Model):
    def sizes(self):
        return super(Variation_manager, self).filter(variation='size')

    def colors(self):
        return super(Variation_manager, self).filter(variation='color')

VARIATION_TYPE = {
    ('size', 'size'),
    ('color', 'color'),
}

class VariationValue(models.Model):
    variation = models.CharField(max_length=100, choices=VARIATION_TYPE)
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    objects = Variation_manager()
    def __str__(self):
        return self.name