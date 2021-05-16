from django.db import models
from datetime import datetime

from company.models import Company

class Stock(models.Model):
    class Meta:
        unique_together = (('company', 'record_date'),)

    record_date = models.DateTimeField(null=True, default=None)
    open = models.FloatField(default= -1)
    high = models.FloatField(default= -1)
    low = models.FloatField(default= -1)
    close = models.FloatField(default= -1)
    volume = models.FloatField(default= -1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

