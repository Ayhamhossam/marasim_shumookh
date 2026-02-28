from django.contrib import admin
from django.urls import path

admin.site.site_header = "مراسيم الشموخ"
admin.site.site_title = "نظام الإدارة"

urlpatterns = [
    path('admin/', admin.site.urls),
]
