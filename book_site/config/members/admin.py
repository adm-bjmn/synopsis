from django.contrib import admin
from django.contrib.auth.models import Group, User

# Register your models here.


# unregister
admin.site.unregister(Group)

# Just display username on admin site
