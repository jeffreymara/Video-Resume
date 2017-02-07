from django.contrib import admin
from videoresume.models import User_Info, File, Company, Blocked_Company, Job_Location, Role, Sub_Role

# Register your models here.
admin.site.register(User_Info)
admin.site.register(File)
admin.site.register(Company)
admin.site.register(Blocked_Company)
admin.site.register(Job_Location)
admin.site.register(Role)
admin.site.register(Sub_Role)