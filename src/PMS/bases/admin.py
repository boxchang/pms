from django.contrib import admin

from bases.models import Status, FormType
from bugs.models import Bug
from helpdesk.models import HelpdeskType
from problems.models import Problem, Problem_reply
from projects.models import Project, Project_setting
from requests.models import Request, Level
from tests.models import Request_test, Request_test_item


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