from django.db import models
from django.utils import timezone
from typing import Optional

class Brand(models.Model):
    name: str = models.CharField(max_length=255)
    daily_budget: float = models.FloatField(default=0.0)
    monthly_budget: float = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.name


class Campaign(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=255)
    is_active: bool = models.BooleanField(default=True)
    start_hour: int = models.IntegerField(default=0)  # 0 to 23
    end_hour: int = models.IntegerField(default=23)

    def is_within_daypart(self, now: Optional[timezone.datetime] = None) -> bool:
        if now is None:
            now = timezone.now()
        current_hour = now.hour
        return self.start_hour <= current_hour <= self.end_hour

    def __str__(self) -> str:
        return self.name


class Spend(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    daily_spend: float = models.FloatField(default=0.0)
    monthly_spend: float = models.FloatField(default=0.0)
    last_updated: timezone.datetime = models.DateTimeField(auto_now=True)

    def reset_daily(self) -> None:
        self.daily_spend = 0.0
        self.save()

    def reset_monthly(self) -> None:
        self.monthly_spend = 0.0
        self.save()

    def increment(self, amount: float) -> None:
        self.daily_spend += amount
        self.monthly_spend += amount
        self.save()

    def __str__(self) -> str:
        return f"Spend for {self.campaign.name}"
