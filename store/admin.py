from django.contrib import admin
from .models import Product, Sale

@admin.register(Product)
class PAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'stock')

@admin.register(Sale)
class SAdmin(admin.ModelAdmin):
    list_display = ('product', 'qty', 'sale_price', 'date')
    list_filter = ('date',)
