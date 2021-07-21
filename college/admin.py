from django.contrib import admin

# Register your models here.

from .models import MyProfile,CollegeData

admin.site.register(MyProfile)
admin.site.register(CollegeData)