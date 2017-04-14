from django.contrib import admin

from .models import Activity, FieldOfEducation, Material, Image, File, MaterialAmount


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class MaterialAmountInline(admin.TabularInline):
    model = MaterialAmount
    extra = 1


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = ("title", ("min_age", "max_age"), ("groupsize_min", "groupsize_max"),
              "field_of_education", "seasons", "setting", "tags", "description", "source")
    readonly_fields = ("tags",)
    filter_horizontal = ("field_of_education",)
    search_fields = ("title", "description")
    inlines= [MaterialAmountInline, ImageInline, FileInline]


admin.site.register((FieldOfEducation, Material))
