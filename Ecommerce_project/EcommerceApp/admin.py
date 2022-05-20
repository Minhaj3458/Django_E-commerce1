from django.contrib import admin
from .import models
# Register your models here.

class ProductImageAdmin(admin.StackedInline):
    model = models.ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(models.Category)

admin.site.register(models.Product,ProductAdmin)

admin.site.register(models.Profile)

admin.site.register(models.Cart)

admin.site.register(models.Order)

admin.site.register(models.VariationValue)