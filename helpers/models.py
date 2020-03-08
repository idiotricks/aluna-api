from datetime import datetime

from django.db import models


def auto_number(object_model, prefix='PRD'):
    counter = object_model.objects.all().last().pk + 1
    return datetime.now().strftime(f'{prefix}-%d%m%Y-{"%05d" % counter}')

