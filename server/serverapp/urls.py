from django.conf.urls import url

from serverapp.Views import LoginView
from serverapp.Views import ItemsView
from serverapp.Views import SellView
from serverapp.Views import BuyView
from serverapp.Views import UserInfo

urlpatterns = [
    url(r'^login$', LoginView.login),
    url(r'^items$', ItemsView.items),
    url(r'^sell$', SellView.sell),
    url(r'^buy$', BuyView.buy),
    url(r'^user_info$', UserInfo.user_info),
]
