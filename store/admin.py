from django.contrib import admin
from .models import Product, Sale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_price', 'stock', 'view_profit')
    search_fields = ('name',)

    def view_profit(self, obj):
        return f"{obj.product_profit()} ريال"
    view_profit.short_description = "صافي الربح"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'qty', 'sale_price', 'get_total', 'get_net_profit', 'date')
    list_filter = ('date', 'product')
    date_hierarchy = 'date'
    search_fields = ('product__name',)

    def get_total(self, obj):
        return obj.qty * obj.sale_price
    get_total.short_description = "إجمالي العملية"

    def get_net_profit(self, obj):
        profit = (obj.sale_price - obj.product.cost_price) * obj.qty
        return f"{profit} ريال"
    get_net_profit.short_description = "الربح الصافي"
