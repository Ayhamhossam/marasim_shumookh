from django.contrib import admin
from .models import Product, Sale
from django.utils.timezone import now
from django.db.models import Sum, F

admin.site.site_header = "نظام مراسيم الشموخ للملابس"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_price', 'stock', 'display_sold_qty', 'display_profit')
    search_fields = ('name',)
    list_editable = ('stock',)

    def display_sold_qty(self, obj): return obj.total_sold_qty()
    display_sold_qty.short_description = "المباع"

    def display_profit(self, obj): return f"{obj.total_product_profit()} ريال"
    display_profit.short_description = "أرباح المنتج"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'qty', 'sale_price', 'get_profit', 'date', 'note')
    list_filter = ('date', 'product')
    date_hierarchy = 'date'
    
    def get_profit(self, obj):
        return f"{obj.net_profit} ريال"
    get_profit.short_description = "الربح الصافي"

    def changelist_view(self, request, extra_context=None):
        today = now().date()
        today_sales = Sale.objects.filter(date__date=today)
        extra_context = extra_context or {}
        extra_context['today_count'] = today_sales.count()
        extra_context['today_total'] = today_sales.aggregate(total=Sum(F('sale_price') * F('qty')))['total'] or 0
        extra_context['today_profit'] = sum(s.net_profit for s in today_sales)
        return super().changelist_view(request, extra_context=extra_context)
