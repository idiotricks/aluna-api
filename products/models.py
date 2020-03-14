from django.contrib.auth.models import User
from django.db import models

from helpers.models import auto_number
from utils.models import Timestamp


class Product(Timestamp):
    PRODUCT_PREFIX = 'PRD'
    numcode = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, default='Ex: Black Tshirt')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='userproduct', blank=True, null=True)
    cogs = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    is_publish = models.BooleanField(default=False)
    is_init = models.BooleanField(default=True)

    def __str__(self):
        return self.numcode

    def save(self, *args, **kwargs):
        if not self.numcode:
            self.numcode = auto_number(Product, self.PRODUCT_PREFIX)
        super(Product, self).save(*args, **kwargs)


