import xadmin
from .xadmin_actions import SchoolLevelAction, ProvincialLevelAction, NationalLevelAction
from .models import Project


class ProjectAdmin(object):
    list_display = ['p_name', 'p_notice', 'p_type',
                    'p_leader', 'expert_group', 'get_member', 'member_num',  'get_score', 'p_level', 'p_status']
    search_fields = ['p_name', 'p_notice', 'p_type', 'p_level',
                     'p_leader', 'p_status']
    list_filter = ['p_name', 'p_notice', 'p_type', 'p_level', 'p_leader']

    # 允许直接在列表页进行编辑
    list_editable = ['expert_group']

    actions = [NationalLevelAction, ProvincialLevelAction, SchoolLevelAction, ]

    model_icon = 'fa fa-list'

xadmin.site.register(Project, ProjectAdmin)
