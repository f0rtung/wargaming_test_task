import json
from functools import wraps
from django.http import JsonResponse

from ..Responses.BaseResponses import BaseResponse, ErrorResponse, SuccessResponse


def json_response(func):
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        try:
            result = func(request, *args, **kwargs)
            if isinstance(result, dict):
                response = SuccessResponse().as_dict()
                response.update(result)
            elif issubclass(type(result), BaseResponse):
                response = result.as_dict()
            else:
                raise TypeError("Can not create json response from {}".format(type(result)))
        except Exception as err:
            response = ErrorResponse(err).as_dict()
        return JsonResponse(response, status=200)

    return func_wrapper


def check_post_method(func):
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        else:
            return ErrorResponse("Invalid method ({}) !".format(request.method))
    return func_wrapper
