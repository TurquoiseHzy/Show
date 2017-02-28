from django.contrib import admin

from .models import *

admin.AdminSite.site_header = 'Giligili'
admin.site.register(Video)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(UserExtraProfile)