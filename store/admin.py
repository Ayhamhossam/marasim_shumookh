from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Sale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # ترتيب الأعمدة ليكون السعر واضحاً جداً
    list_display = ('name', 'display_cost', 'display_stock', 'view_profit')
    search_fields = ('name',)
    list_filter = ('stock',)

    def display_cost(self, obj):
        return format_html('<span style="color: #17a2b8; font-weight: bold;">{} ريال</span>', obj.cost_price)
    display_cost.short_description = "سعر الشراء"

    def display_stock(self, obj):
        color = "red" if obj.stock <= 5 else "black"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.stock)
    display_stock.short_description = "المخزون"

    def view_profit(self, obj):
        profit = obj.product_profit()
        return format_html('<span style="color: #28a745; font-weight: bold;">+ {} ريال</span>', profit)
    view_profit.short_description = "صافي ربح الصنف"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'qty', 'display_sale_price', 'get_total', 'get_net_profit', 'date')
    list_filter = ('date', 'product')
    autocomplete_fields = ['product'] # بحث سريع عن المنتج
    
    def display_sale_price(self, obj):
        return f"{obj.sale_price} ريال"
    display_sale_price.short_description = "سعر البيع"

    def get_total(self, obj):
        return f"{obj.qty * obj.sale_price} ريال"
    get_total.short_description = "الإجمالي"

    def get_net_profit(self, obj):
        profit = (obj.sale_price - obj.product.cost_price) * obj.qty
        color = "#28a745" if profit > 0 else "#dc3545"
        return format_html('<span style="color: {}; font-weight: bold;">{} ريال</span>', color, profit)
    get_net_profit.short_description = "الربح الصافي"
