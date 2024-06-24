# store/management/commands/create_timeslots.py
# -*- coding: utf-8 -*-
import datetime
from django.core.management.base import BaseCommand
from store.models import TimeSlot

class Command(BaseCommand):
    help = 'Create time slots for a given date range'

    def handle(self, *args, **kwargs):
        start_date = datetime.date(2024, 6, 27)
        end_date = datetime.date(2024, 7, 31)
        start_time = datetime.time(18, 0)
        end_time = datetime.time(20, 0)
        delta = datetime.timedelta(days=1)

        while start_date <= end_date:
            TimeSlot.objects.create(date=start_date, start_time=start_time, end_time=end_time, available=True)
            start_date += delta

        self.stdout.write(self.style.SUCCESS('Successfully created time slots'))
