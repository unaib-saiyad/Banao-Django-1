from django.contrib import admin
from .models import UserInformation, Blog
# Register your models here.

admin.site.register(UserInformation)
admin.site.register(Blog)
