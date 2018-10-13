from .BaseResponses import SuccessResponse


class UserWithItemsResponse(SuccessResponse):
    def __init__(self, user, items):
        super().__init__()
        self._user = user
        self._items = items

    def as_dict(self):
        response = super().as_dict()
        response['user'] = self._user.as_dict()
        response['items'] = [
            item.item.as_dict()
            for item in self._items
        ]
        return response
