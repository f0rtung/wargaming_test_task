import requests
from abc import ABC, abstractmethod


def input_strip_text(input_check_callback, on_fail_text):
    user_input = input().strip()
    while not user_input or not input_check_callback(user_input):
        print(on_fail_text)
        user_input = input().strip()
    return user_input


def check_response(status_code, json):
    if status_code != 200:
        raise ValueError("Invalid status code: {}".format(status_code))
    try:
        is_ok = json['ok']
        if not is_ok:
            raise ValueError(json['error_message'])
    except KeyError:
        raise ValueError("Invalid json response: ", json)


def print_items(items):
    for item in items:
        print("id: {}, name: '{}', price: {}".format(item['id'], item['name'], item['price']))


def check_positive_int(text):
    try:
        return int(text) >= 0
    except:
        pass
    return False


class State(ABC):
    def __init__(self, url, state_machine):
        self._url = url
        self.state_machine = state_machine

    def make_request_url(self, last_part):
        return "{}/{}".format(self._url, last_part)

    @abstractmethod
    def show_menu(self):
        pass

    @abstractmethod
    def do_request(self):
        pass

    @abstractmethod
    def show_request_result(self):
        pass

    @abstractmethod
    def change_state(self):
        pass


class StateWithUserID(State):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)
        self._user_id = None

    def set_user_id(self, user_id):
        self._user_id = user_id
        assert self._user_id and self._user_id > 0, "User should be valid index"

    def get_user_id(self):
        return self._user_id

    def reset_user_id(self):
        self._user_id = None
