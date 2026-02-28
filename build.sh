#!/usr/bin/env bash
set -o errexit

# تثبيت المكتبات
pip install -r requirements.txt

# تجميع ملفات التنسيق
python manage.py collectstatic --no-input

# إنشاء ملفات الهجرة (التحديث)
python manage.py makemigrations --noinput
python manage.py makemigrations store --noinput

# تطبيق التحديث على قاعدة البيانات (هذا هو السطر المنقذ)
python manage.py migrate --noinput
