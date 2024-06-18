from django.contrib import admin
from django.contrib.auth.models import Group

from . import models

# Register your models here.
admin.site.unregister(Group)
admin.site.register(models.User)
