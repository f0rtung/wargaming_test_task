from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from ..Utils.RequestWrapper import RequestWrapper
from ..Models.UsersModel import get_existing_user
from ..Models.ItemsModel import get_existing_item
from ..Models.UserItemModel import remove_user_item
from ..Responses.BaseResponses import SuccessResponse
from ..Utils.Decorators import json_response, check_post_method


@csrf_exempt
@json_response
@check_post_method
def sell(request):
    rw = RequestWrapper(request)
    user = get_existing_user(rw.user_id())
    item = get_existing_item(rw.item_id())
    with transaction.atomic():
        remove_user_item(user, item)
        user.credit += item.price
        user.save()
    return SuccessResponse()
