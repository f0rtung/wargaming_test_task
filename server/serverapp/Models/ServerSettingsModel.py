from random import uniform
from django.db import models


def random_start_credit():
    try:
        min_credit = ServerSettingsModel.objects.get(name='start_credit_min')
        max_credit = ServerSettingsModel.objects.get(name='start_credit_max')
        return round(uniform(min_credit.as_float(), max_credit.as_float()), 2)
    except Exception:
        pass
    return 0


class ServerSettingsModel(models.Model):
    name = models.CharField(max_length=1024)
    value = models.CharField(max_length=1024)

    class Meta:
        db_table = 'server_settings'

    def __str__(self):
        return "setting name: '{}', value: {}".format(self.name, self.value)

    def as_float(self):
        return float(self.value)
