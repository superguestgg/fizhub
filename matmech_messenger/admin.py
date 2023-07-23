from django.contrib import admin
from .models import Guest, PrivateChat, PrivateMessage, GuestSession

for model in [Guest, PrivateChat, PrivateMessage, GuestSession]:
    admin.site.register(model)


# Register your models here.
