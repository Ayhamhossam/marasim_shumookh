from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class Product(models.Model):
    name = models.CharField("اسم القطعة", max_length=200)
    cost_price = models.DecimalField("سعر التكلفة", max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField("الكمية المتوفرة", default=0)

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def total_sold_qty(self):
        return self.sale_set.aggregate(Sum('qty'))['qty__sum'] or 0

    def total_product_profit(self):
        sales = self.sale_set.all()
        return sum(((s.sale_price or 0) - (self.cost_price or 0)) * (s.qty or 0) for s in sales)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    qty = models.IntegerField("الكمية المباعة", default=1)
    sale_price = models.DecimalField("سعر البيع اليدوي", max_digits=10, decimal_places=2)
    note = models.TextField("ملاحظة البيع", blank=True, null=True)
    date = models.DateTimeField("وقت البيع", default=timezone.now)

    def save(self, *args, **kwargs):
        if self.product:
            self.product.stock -= self.qty
            self.product.save()
        super().save(*args, **kwargs)

    @property
    def net_profit(self):
        cost = self.product.cost_price or 0
        price = self.sale_price or 0
        return (price - cost) * (self.qty or 0)

@receiver(post_migrate)
def set_permissions(sender, **kwargs):
    if sender.name == 'store':
        try:
            # تحديث صلاحيات علي
            ali, created = User.objects.get_or_create(username='ali')
            if created: ali.set_password('776940187')
            ali.is_staff = True
            ali.save()
            content_types = ContentType.objects.get_for_models(Product, Sale).values()
            permissions = Permission.objects.filter(content_type__in=content_types)
            ali.user_permissions.set(permissions)
        except: pass
