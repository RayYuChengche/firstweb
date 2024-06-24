# create_timeslots.py
# -*- coding: utf-8 -*-
import os
import django
import datetime
from store.models import TimeSlot

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_website.settings")
django.setup()

# 创建一个日期和时间段的范围
start_date = datetime.date(2024, 6, 27)
end_date = datetime.date(2024, 7, 31)
start_time = datetime.time(18, 0)
end_time = datetime.time(20, 0)
delta = datetime.timedelta(days=1)

while start_date <= end_date:
    TimeSlot.objects.create(date=start_date, start_time=start_time, end_time=end_time, available=True)
    start_date += delta

print("Successfully created time slots")
