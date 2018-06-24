from xadmin.plugins.actions import BaseActionView
from django.utils.translation import gettext as _


class SchoolLevelAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "school_level"    #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    description = _(u'将所选的 %(verbose_name_plural)s 设置为校级立项')

    model_perm = 'change'

    icon = 'fa fa-tasks'

    def do_action(self, queryset):
        for project in queryset:
            project.p_status = '3'
            project.p_level = '1'
            project.deadline = project.p_notice.deadline
            project.save()
        # Return None to display the change list page again.
        return None


class ProvincialLevelAction(BaseActionView):
    action_name = "provincial_level"
    description = _(u'将所选的 %(verbose_name_plural)s 设置为省级立项')
    model_perm = 'change'

    icon = 'fa fa-tasks'

    def do_action(self, queryset):
        for project in queryset:
            project.p_status = '3'
            project.p_level = '2'
            project.deadline = project.p_notice.deadline
            project.save()
        # Return None to display the change list page again.
        return None


class NationalLevelAction(BaseActionView):
    action_name = "national_level"
    description = _(u'将所选的 %(verbose_name_plural)s 设置为国家级立项')
    model_perm = 'change'

    def do_action(self, queryset):
        for project in queryset:
            project.p_status = '3'
            project.p_level = '3'
            project.deadline = project.p_notice.deadline
            project.save()
        # Return None to display the change list page again.
        return None


