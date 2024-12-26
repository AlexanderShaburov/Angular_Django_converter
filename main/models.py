from django.db import models
from django.utils.timezone import now

# Create your models here.

class Currency(models.Model):
    iso_code = models.CharField(
        primary_key=True,
        max_length=4,
        )
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=4)
    pass

class Request(models.Model):
    datetime = models.DateTimeField()
    pass

class Country(models.Model):
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    flag = models.TextField()
    pass

class Rate(models.Model):
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE
    )
    request_id = models.ForeignKey(
        to=Request,
        on_delete=models.CASCADE
    )
    rate = models.FloatField()
    pass
 
    
class Conversion(models.Model):
    currency_source = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name="rate_source"
    )
    currency_target = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE
    )
    amount_source = models.FloatField()
    amount_target = models.FloatField()
    rate_source = models.ForeignKey(
        to=Rate,
        on_delete=models.CASCADE,
        related_name="currency_source"
    )
    rate_target = models.ForeignKey(
        to=Rate,
        on_delete=models.CASCADE
    )
    convert_date = models.DateTimeField(default=now)
    pass
