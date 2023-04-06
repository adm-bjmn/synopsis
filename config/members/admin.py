from django.contrib import admin
from django.contrib.auth.models import Group, User
from members.models import Member


# unregister Groups - Not needed
admin.site.unregister(Group)
# unregister default user
admin.site.unregister(User)
# Just display username on admin site
# admin.site.register(Member)
# combine user and Member


class UserProfile(admin.StackedInline):
    model = Member


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name',
              'last_name', 'password', 'is_staff']
    inlines = [UserProfile]


# register User with new format
admin.site.register(User, UserAdmin)
