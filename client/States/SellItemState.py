import requests
from States.States import StateWithUserID, input_strip_text, check_positive_int, check_response


class SellItemState(StateWithUserID):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)
        self._item_id = None

    def show_menu(self):
        print("Which item id do you want to sell (0 - exit): ")
        self._item_id = int(input_strip_text(check_positive_int,
                                             "Item id should be in positive number, please try again:"))

    def do_request(self):
        if self._item_id == 0:
            return
        response = requests.post(self.make_request_url("sell"),
                                 data={'user_id': self.get_user_id(),
                                       'item_id': self._item_id})
        check_response(response.status_code, response.json())

    def show_request_result(self):
        print()

    def change_state(self):
        self.state_machine.curr_state = self.state_machine.menu_state
