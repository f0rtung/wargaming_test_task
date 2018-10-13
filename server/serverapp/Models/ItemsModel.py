from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ..Utils.Validators import validate_decimals


def all_items():
    return ItemsModel.objects.all()


def get_existing_item(item_id):
    try:
        return ItemsModel.objects.get(id=item_id)
    except ObjectDoesNotExist:
        raise ValueError("Item with id '{}' does not exist".format(item_id))


class ItemsModel(models.Model):
    name = models.CharField(max_length=1024)
    price = models.FloatField(validators=[validate_decimals])

    class Meta:
        db_table = 'items'

    def __str__(self):
        return "name: '{}', price: {}".format(self.name, self.price)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }
