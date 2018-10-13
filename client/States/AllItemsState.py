import requests
from States.States import State, check_response, print_items


class AllItemsState(State):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)
        self._json_response = None

    def show_menu(self):
        pass

    def do_request(self):
        response = requests.get(self.make_request_url("items"))
        self._json_response = response.json()
        check_response(response.status_code, self._json_response)

    def show_request_result(self):
        print("All items:")
        print_items(self._json_response['items'])
        print()

    def change_state(self):
        self.state_machine.curr_state = self.state_machine.menu_state
