from django.contrib import admin

from .models import Activity, FieldOfEducation, Material, Image, File, MaterialAmount

# Register your models here.

admin.site.register((Activity, FieldOfEducation, Material, Image, File, MaterialAmount))