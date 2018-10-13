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

    def run(self):
        while True:
            try:
                self.curr_state.show_menu()
                self.curr_state.do_request()
                self.curr_state.show_request_result()
                self.curr_state.change_state()
            except Exception as err:
                print("Some error: ", err)
