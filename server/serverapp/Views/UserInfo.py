from ..Models.UserItemModel import user_items
from ..Utils.Decorators import json_response
from ..Models.UsersModel import get_existing_user
from ..Utils.RequestWrapper import RequestWrapper
from ..Responses.UserWithItemsResponse import UserWithItemsResponse


@json_response
def user_info(request):
    rw = RequestWrapper(request)
    user_id = rw.user_id()
    user = get_existing_user(user_id)
    items = user_items(user)
    return UserWithItemsResponse(user, items)
