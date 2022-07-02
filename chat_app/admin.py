from django.contrib import admin
from .models import ChatMessages, UserProfile

admin.site.register(UserProfile)
admin.site.register(ChatMessages)
