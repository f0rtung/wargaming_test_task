class RequestWrapper:
    def __init__(self, request):
        if request.method == 'POST':
            self._params = request.POST
        elif request.method == 'GET':
            self._params = request.GET
        else:
            raise ValueError("Unsupported request type: ", request.method)

    def _get_required_str(self, key):
        try:
            return self._params[key]
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
