from django.contrib import admin
from .models import Brand, Campaign, Spend
from celery import shared_task


@shared_task
def reset_daily_spends() -> None:
    for spend in Spend.objects.all():
        spend.reset_daily()


@shared_task
def reset_monthly_spends() -> None:
    for spend in Spend.objects.all():
        spend.reset_monthly()
