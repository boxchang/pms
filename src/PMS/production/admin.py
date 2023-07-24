from django.contrib import admin

from production.models import WorkType


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('type_code', 'type_name')
