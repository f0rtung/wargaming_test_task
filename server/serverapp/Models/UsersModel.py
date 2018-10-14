from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ..Models.ServerSettingsModel import random_start_credit


def get_or_create_user(user_nickname):
    try:
        user = UsersModel.objects.get(nickname=user_nickname)
    except ObjectDoesNotExist:
        random_credit = random_start_credit()
        user = UsersModel.objects.create(nickname=user_nickname, credit=random_credit)
    return user


def get_existing_user(user_id):
    try:
        return UsersModel.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ValueError("User with id '{}' does not exist".format(user_id))


class UsersModel(models.Model):
    nickname = models.CharField(max_length=1024)
    credit = models.FloatField()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return "name: {}, credit: {}".format(self.nickname, self.credit)

    def as_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'credit': self.credit
        }

    def _update_credit(self, value):
        self.credit = round(value, 2)
        self.save(update_fields=["credit"])

    def increase_credit(self, value):
        self._update_credit(self.credit + value)

    def decrease_credit(self, value):
        self._update_credit(self.credit - value)
