from django.contrib import admin

from requestdata_ex_learn.models import Registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['id','frist_name','last_name','email']
# Register your models here.
admin.site.register(Registration,RegistrationAdmin)