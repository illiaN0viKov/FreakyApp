from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Event

class ProfileInLine(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInLine]
    fields = ["username"]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Event)