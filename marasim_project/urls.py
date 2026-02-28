from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/admin/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect),
]
