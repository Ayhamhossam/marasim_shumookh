from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField("اسم المنتج", max_length=200)
    cost = models.DecimalField("سعر التكلفة", max_digits=10, decimal_places=2)
    stock = models.IntegerField("المخزون", default=0)

    def __str__(self): return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    sale_price = models.DecimalField("سعر البيع المنفذ", max_digits=10, decimal_places=2)
    qty = models.IntegerField("الكمية المباعة")
    note = models.TextField("ملاحظة", blank=True)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.product.stock -= self.qty
        self.product.save()
        super().save(*args, **kwargs)
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User

def create_users(sender, **kwargs):
    if not User.objects.filter(username='ayham').exists():
        User.objects.create_superuser('ayham', 'ayham@test.com', '01222560')
    if not User.objects.filter(username='ali').exists():
        user = User.objects.create_user('ali', 'ali@test.com', '776940187')
        user.is_staff = True
        user.save()

post_migrate.connect(create_users)
