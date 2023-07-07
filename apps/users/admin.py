from django.contrib import admin
from apps.users.models import User, ConfirmCode, ResetPasswordCode

admin.site.register(User)
admin.site.register(ConfirmCode)
admin.site.register(ResetPasswordCode)
