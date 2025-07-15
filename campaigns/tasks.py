from celery import shared_task
from django.utils import timezone
from .models import Campaign, Spend

@shared_task
def enforce_budget_limits() -> None:
    now = timezone.now()
    for campaign in Campaign.objects.select_related("brand").all():
        try:
            spend = Spend.objects.get(campaign=campaign)
        except Spend.DoesNotExist:
            continue

        over_daily = spend.daily_spend >= campaign.brand.daily_budget
        over_monthly = spend.monthly_spend >= campaign.brand.monthly_budget
        within_daypart = campaign.is_within_daypart(now)

        if over_daily or over_monthly or not within_daypart:
            if campaign.is_active:
                campaign.is_active = False
                campaign.save()
        else:
            if not campaign.is_active:
                campaign.is_active = True
                campaign.save()