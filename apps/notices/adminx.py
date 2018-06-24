import xadmin
from .models import Notice, NoticeResource


class NoticeResourceInline(object):
    model = NoticeResource
    extra = 0


class NoticeAdmin(object):
    list_display = ['name', 'type', 'desc', 'start_time', 'end_time', 'deadline']
    search_fields = ['name', 'type', 'desc', 'start_time', 'end_time']
    list_filter = ['name', 'type', 'desc', 'start_time', 'end_time']

    model_icon = 'fa fa-bullhorn'

    inlines = [NoticeResourceInline]


class ResourceAdmin(object):
    pass

xadmin.site.register(Notice, NoticeAdmin)
xadmin.site.register(NoticeResource, ResourceAdmin)

