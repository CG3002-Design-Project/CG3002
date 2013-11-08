from django.db import models
from django.contrib import admin
from Display.models import Display

class DisplayAdmin(admin.ModelAdmin):
	list_display =('barcode','display_id')
	search_fields =('barcode','display_id')
	
admin.site.register(Display, DisplayAdmin)