from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employe


admin.site.register(Employe, UserAdmin)