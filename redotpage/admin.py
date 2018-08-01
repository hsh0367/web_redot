from django.contrib import admin
from .models import *

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ['number','user_id','board_title','message','create_date','hit','modify_date']
    list_filter = ['number','user_id','board_title','hit','create_date']


admin.site.register(Board,BoardAdmin)
