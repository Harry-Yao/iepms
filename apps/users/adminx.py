import xadmin
from xadmin import views
from .models import ExpertGroup, UserProfile


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = '创新创业管理后台'
    # 设置base_site.html的Footer
    site_footer = '教务处'
    menu_style = "accordion"
    show_bookmarks = False


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class ExpertGroupAdmin(object):
    model_icon = 'fa fa-users'


class UserProfileAdmin(object):
    list_display = ['username', 'email', 'college', 'user_type', 'expert_group']
    search_fields = ['username', 'email', 'college', ]
    list_filter = ['username', 'user_type', 'college',  'expert_group']

    # 允许直接在列表页进行编辑
    list_editable = ['expert_group']
    model_icon = 'fa fa-user'

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)

xadmin.site.register(ExpertGroup, ExpertGroupAdmin)
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
