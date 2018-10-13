from django.contrib import admin

from serverapp.Models.ServerSettingsModel import ServerSettingsModel
from serverapp.Models.UsersModel import UsersModel
from serverapp.Models.ItemsModel import ItemsModel

admin.site.register(ServerSettingsModel)
admin.site.register(UsersModel)
admin.site.register(ItemsModel)
