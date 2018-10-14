from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from ..Utils.RequestWrapper import RequestWrapper
from ..Models.UsersModel import get_existing_user
from ..Models.ItemsModel import get_existing_item
from ..Models.UserItemModel import create_user_item
from ..Responses.BaseResponses import SuccessResponse
from ..Utils.Decorators import json_response, check_post_method
from ..Responses.NotEnoughMoneyResponse import NotEnoughMoneyResponse


@csrf_exempt
@json_response
@check_post_method
def buy(request):
    rw = RequestWrapper(request)
    user = get_existing_user(rw.user_id())
    item = get_existing_item(rw.item_id())
    if user.credit < item.price:
        return NotEnoughMoneyResponse(user, item)
    with transaction.atomic():
            create_user_item(user, item)
            user.decrease_credit(item.price)
    return SuccessResponse()
