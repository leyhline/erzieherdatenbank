from django.contrib import admin

from .models import Activity, FieldOfEducation, Material, Image, File, MaterialAmount, Festival


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class FileInline(admin.TabularInline):
    model = File
    extra = 0


class MaterialAmountInline(admin.TabularInline):
    model = MaterialAmount
    extra = 0


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = ("title", ("min_age", "max_age"), ("groupsize_min", "groupsize_max"),
              "field_of_education", "festivals", "seasons", "setting", "tags", "description", "source")
    readonly_fields = ("tags",)
    filter_horizontal = ("field_of_education", "festivals")
    search_fields = ("title", "description")
    inlines= [MaterialAmountInline, ImageInline, FileInline]


admin.site.register((FieldOfEducation, Material, Festival))
