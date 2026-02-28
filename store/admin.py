from django.contrib import admin
from .models import Product, Sale

# تغيير عنوان لوحة التحكم
admin.site.site_header = "نظام مراسيم الشموخ للمحاسبة"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # عرض البيانات بدون تعديل خارجي (للحماية)
    list_display = ('name', 'cost_price', 'stock', 'get_profit')
    search_fields = ('name',)

    def get_profit(self, obj):
        return f"{obj.product_profit()} ريال"
    get_profit.short_description = "صافي ربح المنتج"

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # إضافة فلاتر التاريخ والمنتج على اليسار
    list_display = ('product', 'qty', 'sale_price', 'get_total_op', 'get_net_profit', 'date')
    list_filter = ('date', 'product') # هذا هو سطر الفلترة المطلوب
    date_hierarchy = 'date' # يضيف شريط زمني في الأعلى
    search_fields = ('product__name',)

    def get_total_op(self, obj):
        return obj.qty * obj.sale_price
    get_total_op.short_description = "إجمالي العملية"

    def get_net_profit(self, obj):
        profit = (obj.sale_price - obj.product.cost_price) * obj.qty
        return f"{profit} ريال"
    get_net_profit.short_description = "صافي الربح"
