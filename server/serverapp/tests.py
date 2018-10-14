import json
from django.test import TestCase
from .Models.ItemsModel import ItemsModel
from .Models.UsersModel import get_or_create_user
from .Models.UserItemModel import create_user_item


class LoginViewTests(TestCase):
    def test_new_login_without_user_nickname(self):
        response = self.client.post('/server/login')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], False)
        self.assertEqual(response_json['error_message'], "Parameter 'user_nickname' is required")

    def test_new_login_with_new_user_nickname(self):
        nick_name = 'test user'
        response = self.client.post('/server/login', data={'user_nickname': nick_name})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        self.assertEqual(response_json['user']['nickname'], nick_name)
        self.assertEqual(response_json['items'], [])

    def test_new_login_with_existing_user_nickname(self):
        nick_name = 'test user'
        existing_user = get_or_create_user(nick_name)
        item = ItemsModel.objects.create(name="new item", price=12.4)
        create_user_item(existing_user, item)
        nick_name = 'test user'
        response = self.client.post('/server/login', data={'user_nickname': nick_name})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        self.assertEqual(response_json['user']['nickname'], nick_name)
        self.assertEqual(response_json['items'], [{'id': 1, 'name': 'new item', 'price': 12.4}])


class ItemsViewTests(TestCase):
    def test_empty_items(self):
        response = self.client.get('/server/items')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        self.assertEqual(response_json['items'], [])

    def test_items(self):
        ItemsModel.objects.create(name="new item", price=12.4)
        response = self.client.get('/server/items')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        self.assertEqual(response_json['items'], [{'id': 1, 'name': 'new item', 'price': 12.4}])


def _test_without_params(test_self, url):
    response = test_self.client.post(url)
    test_self.assertEqual(response.status_code, 200)
    response_json = json.loads(str(response.content, encoding='utf8'))
    test_self.assertEqual(response_json['ok'], False)


def _test_with_invalid_user_id(test_self, url):
    invalid_user_id = 1
    response = test_self.client.post(url, data={'user_id': invalid_user_id})
    test_self.assertEqual(response.status_code, 200)
    response_json = json.loads(str(response.content, encoding='utf8'))
    test_self.assertEqual(response_json['ok'], False)
    test_self.assertEqual(response_json['error_message'], "User with id '{}' does not exist".format(invalid_user_id))


def _test_without_param_item_id(test_self, url):
    user = get_or_create_user('test user')
    response = test_self.client.post(url, data={'user_id': user.id})
    test_self.assertEqual(response.status_code, 200)
    response_json = json.loads(str(response.content, encoding='utf8'))
    test_self.assertEqual(response_json['ok'], False)
    test_self.assertEqual(response_json['error_message'], "Parameter 'item_id' is required")


def _test_with_invalid_param_item_id(test_self, url):
    invalid_item_id = 12
    user = get_or_create_user('test user')
    response = test_self.client.post(url, data={'user_id': user.id, 'item_id': invalid_item_id})
    test_self.assertEqual(response.status_code, 200)
    response_json = json.loads(str(response.content, encoding='utf8'))
    test_self.assertEqual(response_json['ok'], False)
    test_self.assertEqual(response_json['error_message'], "Item with id '{}' does not exist".format(invalid_item_id))


def _test_without_param_user_id(test_self, url):
    item = ItemsModel.objects.create(name="new item", price=12.4)
    response = test_self.client.post(url, data={'item_id': item.id})
    test_self.assertEqual(response.status_code, 200)
    response_json = json.loads(str(response.content, encoding='utf8'))
    test_self.assertEqual(response_json['ok'], False)
    test_self.assertEqual(response_json['error_message'], "Parameter 'user_id' is required")


class SellViewTests(TestCase):

    def test_sell_without_params(self):
        _test_without_params(self, '/server/sell')

    def test_sell_with_invalid_user_id(self):
        _test_with_invalid_user_id(self, '/server/sell')

    def test_sell_without_param_item_id(self):
        _test_without_param_item_id(self, '/server/sell')

    def test_sell_without_param_user_id(self):
        _test_without_param_user_id(self, '/server/sell')

    def test_sell_with_invalid_param_item_id(self):
        _test_with_invalid_param_item_id(self, '/server/sell')

    def test_sell_user_has_no_item(self):
        user = get_or_create_user('test user')
        item = ItemsModel.objects.create(name="new item", price=12)
        response = self.client.post('/server/sell', data={'item_id': item.id, 'user_id': user.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], False)
        self.assertEqual(response_json['error_message'],
                         "User '{}' has no item '{}'".format(user.nickname, item.name))

    def test_sell(self):
        user = get_or_create_user('test user')
        item = ItemsModel.objects.create(name="new item", price=12.5)
        create_user_item(user, item)
        old_credit = user.credit
        response = self.client.post('/server/sell', data={'item_id': item.id, 'user_id': user.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        user = get_or_create_user('test user')
        self.assertEqual(user.credit, old_credit + item.price)

    def test_sell_again(self):
        user = get_or_create_user('test user')
        item = ItemsModel.objects.create(name="new item", price=12.5)
        create_user_item(user, item)
        old_credit = user.credit
        response = self.client.post('/server/sell', data={'item_id': item.id, 'user_id': user.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        user = get_or_create_user('test user')
        self.assertEqual(user.credit, old_credit + item.price)
        response = self.client.post('/server/sell', data={'item_id': item.id, 'user_id': user.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], False)
        self.assertEqual(response_json['error_message'], "User 'test user' has no item 'new item'")


class BuyViewTests(TestCase):
    def test_buy_without_params(self):
        _test_without_params(self, '/server/buy')

    def test_buy_with_invalid_user_id(self):
        _test_with_invalid_user_id(self, '/server/buy')

    def test_buy_without_param_item_id(self):
        _test_without_param_item_id(self, '/server/buy')

    def test_buy_without_param_user_id(self):
        _test_without_param_user_id(self, '/server/buy')

    def test_buy_with_invalid_param_item_id(self):
        _test_with_invalid_param_item_id(self, '/server/buy')

    def test_buy_not_enough_money(self):
        user = get_or_create_user('test user')
        item = ItemsModel.objects.create(name="new item", price=user.credit + 1)
        response = self.client.post('/server/buy',
                                    data={'user_id': user.id, 'item_id': item.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], False)
        self.assertEqual(response_json['error_message'],
                         "User '{}' does not have enough money to buy item '{}'".format(user.nickname, item.name))

    def test_buy(self):
        user = get_or_create_user('test user')
        user.credit += 15
        user.save()
        item = ItemsModel.objects.create(name="new item", price=user.credit - 1)
        response = self.client.post('/server/buy',
                                    data={'user_id': user.id, 'item_id': item.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)

    def test_buy_again(self):
        user = get_or_create_user('test user')
        user.credit += 45
        user.save()
        item = ItemsModel.objects.create(name="new item", price=15)
        response = self.client.post('/server/buy',
                                    data={'user_id': user.id, 'item_id': item.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        user = get_or_create_user('test user')
        self.assertEqual(user.credit, 30)

        response = self.client.post('/server/buy',
                                    data={'user_id': user.id, 'item_id': item.id})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], False)
        self.assertEqual(response_json['error_message'],
                         "Can not create item '{}' for user '{}', "
                         "error: UNIQUE constraint failed: user_item.user_id, user_item.item_id"
                         .format(item.name, user.nickname))


class UserInfoTests(TestCase):
    def test_user_info_without_user_id(self):
        response = self.client.get('/server/user_info')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], False)
        self.assertEqual(response_json['error_message'], "Parameter 'user_id' is required")

    def test_user_info_with_invalid_user_id(self):
        invalid_user_id = 11
        response = self.client.get('/server/user_info?user_id={}'.format(invalid_user_id))
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], False)
        self.assertEqual(response_json['error_message'], "User with id '{}' does not exist".format(invalid_user_id))

    def test_user_info(self):
        user_nickname = 'test user'
        user = get_or_create_user(user_nickname)
        user.credit += 15
        user.save()
        response = self.client.get('/server/user_info?user_id={}'.format(user.id))
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        self.assertEqual(response_json['user']['nickname'], user_nickname)
        self.assertEqual(response_json['user']['credit'], 15)
        self.assertEqual(response_json['items'], [])

        item = ItemsModel.objects.create(name="new item", price=12.4)
        create_user_item(user, item)
        response = self.client.get('/server/user_info?user_id={}'.format(user.id))
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(response_json['ok'], True)
        self.assertEqual(response_json['items'], [{'id': 1, 'name': 'new item', 'price': 12.4}])
