class RequestWrapper:
    def __init__(self, request):
        self._post_params = request.POST

    def _get_required_str(self, key):
        try:
            return self._post_params[key]
        except KeyError:
            raise ValueError("Parameter '{}' is required".format(key))

    def _get_required_int(self, key):
        return int(self._get_required_str(key))

    def user_nickname(self):
        return self._get_required_str('user_nickname')

    def user_id(self):
        return self._get_required_int('user_id')

    def item_id(self):
        return self._get_required_int('item_id')
