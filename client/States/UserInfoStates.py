import requests
from States.States import StateWithUserID, check_response, print_items


class UserInfoBaseState(StateWithUserID):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)
        self._json_response = None

    def show_menu(self):
        pass

    def do_request(self):
        response = requests.get(self.make_request_url("user_info?user_id={}".format(self.get_user_id())))
        self._json_response = response.json()
        check_response(response.status_code, self._json_response)

    def change_state(self):
        self.state_machine.curr_state = self.state_machine.menu_state


class UserBalanceState(UserInfoBaseState):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)

    def show_request_result(self):
        print("Your balance:")
        print(self._json_response['user']['credit'])
        print()


class UserItemsState(UserInfoBaseState):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)

    def show_request_result(self):
        print("Your items:")
        print_items(self._json_response['items'])
        print()
