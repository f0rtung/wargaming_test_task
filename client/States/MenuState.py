from States.States import StateWithUserID, input_strip_text


class MenuState(StateWithUserID):
    def __init__(self, url, state_machine):
        super().__init__(url, state_machine)
        self._action = 0

    def show_menu(self):
        print("Please select an action:")
        print("1: Print all items")
        print("2: Print your items")
        print("3: Sell your item")
        print("4: Buy new item")
        print("5: Show your balance")
        print("0: Logout")

        def check_action(text):
            try:
                num = int(text)
                return num in range(1, 6) or num == 0
            except:
                pass
            return False

        self._action = int(input_strip_text(check_action, "Action should be in the range of 1 to 6 or equal to 0, "
                                                          "please try again:"))

    def do_request(self):
        pass

    def show_request_result(self):
        print()

    def change_state(self):
        if self._action == 1:
            self.state_machine.curr_state = self.state_machine.all_items_state
        if self._action == 2:
            self.state_machine.user_items_state.set_user_id(self.get_user_id())
            self.state_machine.curr_state = self.state_machine.user_items_state
        if self._action == 3:
            self.state_machine.sell_item_state.set_user_id(self.get_user_id())
            self.state_machine.curr_state = self.state_machine.sell_item_state
        if self._action == 4:
            self.state_machine.buy_item_state.set_user_id(self.get_user_id())
            self.state_machine.curr_state = self.state_machine.buy_item_state
        if self._action == 5:
            self.state_machine.balance_state.set_user_id(self.get_user_id())
            self.state_machine.curr_state = self.state_machine.balance_state
        if self._action == 0:
            self.reset_user_id()
            self.state_machine.curr_state = self.state_machine.login_state
