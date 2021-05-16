from django.db import models
from datetime import datetime


class Company(models.Model):
    NIFTY50 = "N50"
    DIVIDEND = "DIV"
    COMPANY_TYPES = (
        (NIFTY50, "Nifty 50 listed company"),
        (DIVIDEND, "Good dividend yielding company"),
    )

    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20, unique=True)
    series = models.CharField(max_length=50)
    isin = models.CharField(max_length=50)
    bse_code = models.PositiveIntegerField(null=False)
    type = models.CharField(max_length=3, choices=COMPANY_TYPES, default=NIFTY50)
    remarks = models.CharField(max_length=200, default="")
    price_updated_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)
