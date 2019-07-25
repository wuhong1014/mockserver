from django.contrib import admin
from api.models import RuleInfo,History,Project
# Register your models here.
@admin.register(RuleInfo)
class RuleInfoAdmin(admin.ModelAdmin):
    list_display = ['uid','name','desc','request_body','response_body','proxy','priority','project','create_time','update_time']
    list_filter = ['uid', 'name']
    search_fields = ['uid','name']
    list_per_page = 20
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','name','create_time']
    list_filter = ['id', 'name']
    search_fields = ['id', 'name']
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'rule','request_body','response_body', 'create_time']
    ordering = ('-id',)
    # list_editable 设置默认可编辑字段
    # list_editable = ['rule', 'request_body']