class BaseResponse:
    def __init__(self, is_ok, error_message):
        self._is_ok = is_ok
        self._error_message = error_message

    def as_dict(self):
        return {
            'ok': self._is_ok,
            'error_message': self._error_message
        }


class ErrorResponse(BaseResponse):
    def __init__(self, error_message):
        super().__init__(False, str(error_message))


class SuccessResponse(BaseResponse):
    def __init__(self):
        super().__init__(True, "")

