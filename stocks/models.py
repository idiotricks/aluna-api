from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from helpers.models import auto_number
from products.models import Product
from users.models import Supplier, Customer
from utils.models import Timestamp


class StockCard(Timestamp):
    STOCK_CARD_PREFIX = 'STC'
    numcode = models.CharField(max_length=20)
    date = models.DateField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='productstockcard')
    init_balance = models.PositiveIntegerField(default=0)
    total_in = models.PositiveIntegerField(default=0)
    end_balance = models.PositiveIntegerField(default=0)
    total_out = models.PositiveIntegerField(default=0)
    is_init = models.BooleanField(default=True)

    def __str__(self):
        return self.numcode

    def save(self, *args, **kwargs):
        if not self.numcode:
            self.numcode = auto_number(StockCard, self.STOCK_CARD_PREFIX)
        super(StockCard, self).save(*args, **kwargs)


class StockIn(Timestamp):
    STOCK_IN_PREFIX = 'STI'
    numcode = models.CharField(max_length=20, unique=True)
    date = models.DateField(blank=True, null=True, default=now().date())
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='supplierstockin',
        blank=True,
        null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userstockin')
    is_init = models.BooleanField(default=True)
    is_calculate = models.BooleanField(default=False)

    def __str__(self):
        return self.numcode

    def save(self, *args, **kwargs):
        if not self.numcode:
            self.numcode = auto_number(StockIn, self.STOCK_IN_PREFIX)
        super(StockIn, self).save(*args, **kwargs)


class ItemIn(Timestamp):
    stockin = models.ForeignKey(
        StockIn,
        on_delete=models.CASCADE,
        related_name='stockinitemin',
        blank=True,
        null=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='productitemin',
        blank=True,
        null=True
    )
    stock = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    end_stock = models.PositiveIntegerField(default=0)
    is_init = models.BooleanField(default=True)

    def __str__(self):
        return self.stockin.numcode


class StockOut(Timestamp):
    STOCK_OUT_PREFIX = 'STO'
    numcode = models.CharField(max_length=20, unique=True)
    date = models.DateField(blank=True, null=True, default=now().date())
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='supplierstockout',
        blank=True,
        null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userstockout')
    is_init = models.BooleanField(default=True)
    is_calculate = models.BooleanField(default=False)

    def __str__(self):
        return self.numcode

    def save(self, *args, **kwargs):
        if not self.numcode:
            self.numcode = auto_number(StockOut, self.STOCK_OUT_PREFIX)
        super(StockOut, self).save(*args, **kwargs)


class ItemOut(Timestamp):
    stockout = models.ForeignKey(StockOut, on_delete=models.CASCADE, related_name='stockoutitemout')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productitemout')
    stock = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    is_init = models.BooleanField(default=False)
    end_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.stockout.numcode

