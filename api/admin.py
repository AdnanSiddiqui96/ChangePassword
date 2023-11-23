from django.contrib import admin

# Register your models here.

from api.models import*

admin.site.register(Role)
admin.site.register(Account)
admin.site.register(whitelistToken)
admin.site.register(UserPassword)


