from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField("اسم القطعة", max_length=200)
    cost_price = models.DecimalField("سعر التكلفة (الشراء)", max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField("الكمية المتوفرة", default=0)

    def __str__(self):
        return f"{self.name} - (التكلفة: {self.cost_price} | المخزن: {self.stock})"

    # --- هذه هي الدالة المفقودة التي تسبب الخطأ ---
    def product_profit(self):
        sales = self.sale_set.all()
        # حساب الأرباح: (سعر البيع - سعر التكلفة) * الكمية
        return sum(((s.sale_price or 0) - (self.cost_price or 0)) * (s.qty or 0) for s in sales)

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "1. إدارة الأصناف والمخزن"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="اختر المنتج")
    qty = models.IntegerField("الكمية المباعة", default=1)
    sale_price = models.DecimalField("سعر البيع الحالي", max_digits=10, decimal_places=2)
    date = models.DateTimeField("وقت العملية", default=timezone.now)
    note = models.TextField("ملاحظات إضافية", blank=True, null=True)

    def clean(self):
        # منع البيع بأكثر من المخزن
        if self.product and self.qty > self.product.stock:
            raise ValidationError(f"❌ خطأ: لا يوجد سوى {self.product.stock} قطع في المخزن.")
        # حماية من البيع بخسارة
        if self.product and self.sale_price < self.product.cost_price:
            raise ValidationError(f"⚠️ حماية الخسارة: سعر التكلفة هو {self.product.cost_price}. لا يمكنك البيع بأقل منه!")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.pk: # خصم من المخزن فقط عند أول حفظ
            self.product.stock -= self.qty
            self.product.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "عملية بيع"
        verbose_name_plural = "2. سجل المبيعات والارباح"
