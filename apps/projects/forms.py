from django import forms

from .models import Project, Member


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ['p_leader', 'p_status', 'p_comment', 'p_level', 'p_code', 'financial_appropriation',
                   'college_appropriation', 'expert_group', 'add_time']


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['project']


class MiddleForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['p_middle', 'p_status']




