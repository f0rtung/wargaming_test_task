from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .UsersModel import UsersModel
from .ItemsModel import ItemsModel


def user_items(user):
    query = UserItemModel.objects.select_related('item').filter(user=user)
    return query


def remove_user_item(user, item):
    try:
        user_item = UserItemModel.objects.get(user=user, item=item)
    except ObjectDoesNotExist:
        raise ValueError("User '{}' has no item '{}'".format(user.nickname, item.name))
    user_item.delete()


def create_user_item(user, item):
    try:
        UserItemModel.objects.create(user=user, item=item)
    except Exception as err:
        raise ValueError("Can not create item '{}' for user '{}', error: {}"
                         .format(item.name, user.nickname, err))


class UserItemModel(models.Model):
    user = models.ForeignKey(UsersModel)
    item = models.ForeignKey(ItemsModel)

    class Meta:
        db_table = 'user_item'
        unique_together = ('user', 'item')
