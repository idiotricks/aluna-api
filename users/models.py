from django.db import models

from helpers.models import auto_number
from utils.models import Timestamp


class Customer(Timestamp):
    CUSTOMER_PREFIX = 'CSR'
    numcode = models.CharField(unique=True, max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, default='Ex: Sintia')
    phone = models.CharField(max_length=20, default='Ex: +62xxxxxxxxxx')
    address = models.TextField(default='Ex: Jl. Kartika')
    is_init = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.numcode:
            self.numcode = auto_number(Customer, self.CUSTOMER_PREFIX)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.numcode


class Supplier(Timestamp):
    SUPPLIER_PREFIX = 'SPR'
    numcode = models.CharField(unique=True, max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, default='Ex: Sintia')
    phone = models.CharField(max_length=20, default='Ex: +62xxxxxxxxxx')
    address = models.TextField(default='Ex: Jl. Kartika')
    is_publish = models.BooleanField(default=False)
    is_init = models.BooleanField(default=True)

    def __str__(self):
        return self.numcode

    def save(self, *args, **kwargs):
        if not self.numcode:
            self.numcode = auto_number(Supplier, self.SUPPLIER_PREFIX)
        super(Supplier, self).save(*args, **kwargs)


