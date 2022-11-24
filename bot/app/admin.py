from django.contrib import admin

from .models import DialogState, Question, ChatHistory, BaseStatistic

admin.site.register(DialogState)
admin.site.register(Question)


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'create_at')
    list_filter = ('user',)
    readonly_fields = ('create_at',)


@admin.register(BaseStatistic)
class BaseStatisticAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at',)
    list_display = ('ip_addr', 'create_at')
