import requests
from States.States import State, input_strip_text, check_response, print_items


class LoginState(State):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)
        self._user_nickname = None
        self._json_response = None

    def show_menu(self):
        print("Please enter user nickname:")
        self._user_nickname = input_strip_text(lambda text: True, "User nickname can not be empty, please try again:")
        print()

    def do_request(self):
        response = requests.post(self.make_request_url("login"),
                                 data={'user_nickname': self._user_nickname})
        self._json_response = response.json()
        check_response(response.status_code, self._json_response)

    def show_request_result(self):
        user_stat = self._json_response['user']
        print("Hello, {}!".format(user_stat['nickname']))
        print("Balance: ", user_stat['credit'])
        print("Your items:")
        print_items(self._json_response['items'])
        print()

    def change_state(self):
        user_id = self._json_response['user']['id']
        self.state_machine.set_user_id(user_id)
        self.state_machine.curr_state = self.state_machine.menu_state
