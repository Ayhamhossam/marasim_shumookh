from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField("اسم القطعة", max_length=200)
    cost_price = models.DecimalField("سعر التكلفة", max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField("الكمية المتوفرة", default=0)

    def __str__(self):
        return f"{self.name} (المخزون: {self.stock})"

    # حساب إجمالي الربح لهذا المنتج فقط
    def product_profit(self):
        sales = self.sale_set.all()
        return sum(((s.sale_price or 0) - (self.cost_price or 0)) * (s.qty or 0) for s in sales)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    qty = models.IntegerField("الكمية المباعة", default=1)
    sale_price = models.DecimalField("سعر البيع اليدوي", max_digits=10, decimal_places=2)
    date = models.DateTimeField("وقت البيع", default=timezone.now)
    note = models.TextField("ملاحظة", blank=True, null=True)

    def clean(self):
        # منع البيع لو الكمية مش موجودة
        if self.product and self.qty > self.product.stock:
            raise ValidationError(f"خطأ محاسبي: المخزون لا يكفي! المتوفر {self.product.stock} فقط.")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.pk: # يخصم من المخزن فقط عند البيع الجديد
            self.product.stock -= self.qty
            self.product.save()
        super().save(*args, **kwargs)
