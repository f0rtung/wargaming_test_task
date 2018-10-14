from States.MenuState import MenuState
from States.LoginState import LoginState
from States.BuyItemState import BuyItemState
from States.AllItemsState import AllItemsState
from States.SellItemState import SellItemState
from States.UserInfoStates import UserBalanceState, UserItemsState


class StateMachine:
    def __init__(self, url):
        self.login_state = LoginState(url, self)
        self.menu_state = MenuState(url, self)
        self.all_items_state = AllItemsState(url, self)
        self.user_items_state = UserItemsState(url, self)
        self.sell_item_state = SellItemState(url, self)
        self.buy_item_state = BuyItemState(url, self)
        self.balance_state = UserBalanceState(url, self)
        self.curr_state = self.login_state

        self._states_with_user_id = [
            self.menu_state,
            self.user_items_state,
            self.sell_item_state,
            self.buy_item_state,
            self.balance_state
        ]

    def set_user_id(self, user_id):
        for state in self._states_with_user_id:
            state.set_user_id(user_id)

    def reset_user_id(self):
        for state in self._states_with_user_id:
            state.reset_user_id()

    def run(self):
        while True:
            try:
                self.curr_state.show_menu()
                self.curr_state.do_request()
                self.curr_state.show_request_result()
                self.curr_state.change_state()
            except Exception as err:
                print("Some error: ", err)
