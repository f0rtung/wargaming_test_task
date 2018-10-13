from .BaseResponses import SuccessResponse


class ItemsResponse(SuccessResponse):
    def __init__(self, items):
        super().__init__()
        self._items = items

    def as_dict(self):
        response = super().as_dict()
        response['items'] = [
            item.as_dict()
            for item in self._items
        ]
        return response
