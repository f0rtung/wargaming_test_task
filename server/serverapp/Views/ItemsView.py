from ..Models.ItemsModel import all_items
from ..Utils.Decorators import json_response
from ..Responses.ItemsResponse import ItemsResponse


@json_response
def items(request):
    return ItemsResponse(all_items())
