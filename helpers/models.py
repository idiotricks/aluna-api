from datetime import datetime


def auto_number(object_model, prefix='PRD'):
    if not object_model.objects.all().last():
        counter = 1
    else:
        counter = object_model.objects.all().last().pk + 1
    return datetime.now().strftime(f'{prefix}-%d%m%Y-{"%05d" % counter}')
