from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class Product(models.Model):
    name = models.CharField("اسم القطعة", max_length=200)
    cost_price = models.DecimalField("سعر التكلفة", max_digits=10, decimal_places=2)
    stock = models.IntegerField("الكمية المتوفرة", default=0)

    def __str__(self):
        return f"{self.name} (المخزون: {self.stock})"

    def total_sold_qty(self):
        return self.sale_set.aggregate(Sum('qty'))['qty__sum'] or 0

    def total_product_profit(self):
        sales = self.sale_set.all()
        return sum((s.sale_price - self.cost_price) * s.qty for s in sales)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    qty = models.IntegerField("الكمية المباعة")
    sale_price = models.DecimalField("سعر البيع اليدوي", max_digits=10, decimal_places=2)
    note = models.TextField("ملاحظة البيع", blank=True, null=True)
    date = models.DateTimeField("وقت البيع", default=timezone.now)

    def save(self, *args, **kwargs):
        self.product.stock -= self.qty
        self.product.save()
        super().save(*args, **kwargs)

    @property
    def net_profit(self):
        return (self.sale_price - self.product.cost_price) * self.qty

# كود ترفيع صلاحيات علي برمجياً
@receiver(post_migrate)
def set_permissions(sender, **kwargs):
    try:
        # إنشاء/تحديث يوزر أيهم (المدير)
        if not User.objects.filter(username='ayham').exists():
            User.objects.create_superuser('ayham', '', '01222560')
        
        # إنشاء/تحديث يوزر علي (الكاشير)
        ali, created = User.objects.get_or_create(username='ali')
        if created:
            ali.set_password('776940187')
        ali.is_staff = True
        ali.save()

        # منحه كل الصلاحيات
        content_types = ContentType.objects.get_for_models(Product, Sale).values()
        permissions = Permission.objects.filter(content_type__in=content_types)
        ali.user_permissions.set(permissions)
    except: pass
