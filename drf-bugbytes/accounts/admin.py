from django.contrib import admin
from accounts.models import User, NewUser

admin.site.register(User)
admin.site.register(NewUser)