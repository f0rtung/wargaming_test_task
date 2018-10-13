from .BaseResponses import ErrorResponse


class NotEnoughMoneyResponse(ErrorResponse):
    def __init__(self, user, item):
        error = "User '{}' does not have enough money to buy item '{}'".format(user.nickname, item.name)
        super().__init__(error)
