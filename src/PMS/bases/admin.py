from django.contrib import admin

from bases.models import Status, FormType
from bugs.models import Bug
from helpdesk.models import HelpdeskType
from problems.models import Problem, Problem_reply
from projects.models import Project, Project_setting
from requests.models import Request, Level
from tests.models import Request_test, Request_test_item
from assets.models import *


@admin.register(Request_test)
class RequestTestAdmin(admin.ModelAdmin):
    list_display = ('request', 'desc', 'get_owner', )


@admin.register(Request_test_item)
class RequestTestAdmin(admin.ModelAdmin):
    list_display = ('test', 'item', )


@admin.register(Project_setting)
class ProjectSettingAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'desc')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('request_no', 'title', 'level')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_en', 'level_cn', 'level_desc')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_en', 'status_cn', 'status_desc')



@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('bug_no', 'belong_to', 'title')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('problem_no', 'belong_to', 'title')


@admin.register(Problem_reply)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('problem_no', 'comment')


@admin.register(FormType)
class FormTypeAdmin(admin.ModelAdmin):
    list_display = ('tid', 'type', 'short_name')


@admin.register(HelpdeskType)
class FormTypeAdmin(admin.ModelAdmin):
    list_display = ('tid', 'type')


@admin.register(AssetArea)
class AssetAreaAdmin(admin.ModelAdmin):
    list_display = ('area_name',)


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('category', 'type_name', 'type_code')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_code')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('category', 'brand_name')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_no', 'category', 'type', 'brand', 'model', 'desc', 'area', 'owner_unit', 'keeper_unit', 'keeper_no', 'keeper_name', 'location', 'pur_date', 'pur_price')


@admin.register(AssetStatus)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('status_name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_no', 'unit_name')


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('desc', 'key', 'series')

