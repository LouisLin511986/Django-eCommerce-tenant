from django.contrib import admin
from epaper.models import EPaperEmail


class EPaperEmailAdmin(admin.ModelAdmin):
    search_fields = ['email', ]
    fields = ('email', )
    list_display = ('email', )
    readonly_fields = ('email', )

admin.site.register(EPaperEmail, EPaperEmailAdmin)         # 註冊 EPaperEmail 模型