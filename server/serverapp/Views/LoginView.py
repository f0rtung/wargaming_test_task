from django.views.decorators.csrf import csrf_exempt

from ..Models.UserItemModel import user_items
from ..Utils.RequestWrapper import RequestWrapper
from ..Models.UsersModel import get_or_create_user
from ..Utils.Decorators import json_response, check_post_method
from ..Responses.UserWithItemsResponse import UserWithItemsResponse


@csrf_exempt
@json_response
@check_post_method
def login(request):
    rw = RequestWrapper(request)
    user = get_or_create_user(rw.user_nickname())
    items = user_items(user)
    return UserWithItemsResponse(user, items)
