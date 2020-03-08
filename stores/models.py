from django.contrib.auth.models import User
from django.db import models

from utils.models import Timestamp


class Store(Timestamp):
    numcode = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ownderstore')
    is_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.numcode

