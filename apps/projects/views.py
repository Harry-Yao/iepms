import json
import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ProjectForm, MemberForm, MiddleForm
from .models import Project, Member, Score
from users.models import ExpertGroup


class ListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        search_keywords = request.GET.get('keywords', "")
        projects = {}
        if user.user_type == 0:
            projects = Project.objects.filter(p_leader=user)
        elif user.user_type == 1:
            status = request.GET.get('status', "")
            notice = request.GET.get('notice', "")
            if user.college == 0:
                projects = Project.objects.filter(p_type=0)
            else:
                projects = Project.objects.exclude(p_type=0)

            if status:
                projects = projects.filter(p_status=status)
            if notice:
                projects = projects.filter(p_notice__name__contains=notice)
        elif user.user_type == 2:
            projects = Project.objects.filter(Q(p_status=1) | Q(p_status=2))
        if search_keywords:
            projects = projects.filter(p_name__icontains=search_keywords)

        if not offset:
            offset = 0
        if not limit:
            limit = 10  # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(projects, int(limit))
        page = int(int(offset) / int(limit) + 1)

        return_data = {"total": "", "rows": []}
        if projects.count():
            return_data['total'] = projects.count()

        for project in pageinator.page(page):
            group_name = None
            score = None
            if project.expert_group:
                group_name = project.expert_group.name
            scores = project.score_set.all()
            if scores.count() != 0:
                scores = [s.score for s in scores]
                score = sum(scores)/len(scores)
            return_data['rows'].append({
                'id': project.id,
                'name': project.p_name,
                'type': project.get_p_type_display(),
                'notice': project.p_notice.name,
                'status': project.get_p_status_display(),
                'expert_group': group_name,
                'score': score,
                'deadline': project.deadline.strftime("%Y-%m-%d") if project.deadline else " - "
            })
        return HttpResponse(json.dumps(return_data), content_type='application/json')


class ProjectsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.user_type == 0:
            return render(request, 'projects/students/list.html')
        if user.user_type == 1:
            return render(request, 'projects/managements/list.html')
        if user.user_type == 2:
            return render(request, 'projects/exports/list.html')


class ProjectDetalView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            project_id = request.GET.get('project_id', "")
            project = Project.objects.get(pk=project_id)
            scores = project.score_set
            members = Member.objects.filter(project=project)
            return render(request, 'projects/students/detal.html',
                          {'project': project, 'members': members, 'scores': scores})
        except Exception as e:
            return render(request, 'projects/students/detal.html', {'err': e})


class ApplyView(LoginRequiredMixin, View):
    def get(self, request):
        projectform = ProjectForm()
        formset = formset_factory(MemberForm)
        memberformset = formset()
        return render(request, "projects/students/apply.html", {'projectForm': projectform, 'formset': memberformset})

    def post(self, request):
        projectform = ProjectForm(request.POST, request.FILES)
        have_mamber = request.POST.get("form-TOTAL_FORMS")

        if projectform.is_valid():
            project = projectform.save(commit=False)
            project.p_leader = request.user
            projectform.save()
            if have_mamber != "0":
                formset = formset_factory(MemberForm)
                memberformset = formset(request.POST)
                if memberformset.is_valid():
                    for memberform in memberformset:
                        member = memberform.save(commit=False)
                        member.project = project
                        member.save()
            project.save()
            user = request.user
            user.has_project = True
            user.save()
            return redirect(reverse('project_list'))

        return render(request, "projects/students/apply.html", {'projectform': projectform})


class UpdateView(LoginRequiredMixin, View):
    def get(self, request):
        project_id = request.GET.get("project_id", "")
        project = Project.objects.get(pk=int(project_id))
        members = Member.objects.filter(project=project)
        return render(request, "projects/students/update.html", {'project': project, 'members': members})

    def post(self, request):
        project_id = request.POST.get("id", "")
        project = Project.objects.get(pk=int(project_id))
        projectform = ProjectForm(request.POST, request.FILES, instance=project)
        have_mamber = request.POST.get("form-TOTAL_FORMS")
        if projectform.is_valid():
            projectform.save()
            if have_mamber != "0":
                formset = formset_factory(MemberForm)
                memberformset = formset(request.POST)
                if memberformset.is_valid():
                    Member.objects.filter(project=project).delete()
                    for memberform in memberformset:
                        memberf = memberform.save(commit=False)
                        # p_member = Member.objects.filter(pk=memberf.id).update(member=memberf)
                        # memberform
                        memberf.project = project
                        memberf.save()
            return redirect(reverse('project_list'))
        return render(request, "projects/students/update.html", {'project': project, 'projectform': projectform})


class ApprovalView(LoginRequiredMixin, View):
    def get(self, request):
        project_id = request.GET.get("project_id", "")
        project = Project.objects.get(pk=int(project_id))
        members = Member.objects.filter(project=project)
        return render(request, "projects/managements/approval.html", {'project': project, 'members': members})

    def post(self, request):
        project_id = request.POST.get("id", "")
        project = Project.objects.get(pk=int(project_id))
        p_comment = request.POST.get("p_comment", "")
        if p_comment:
            project.p_comment = p_comment
        project.p_status = int(request.POST.get("p_status"))
        project.save()
        return redirect(reverse('project_list'))


class GradeView(LoginRequiredMixin, View):
    def get(self, request):
        project_id = request.GET.get("project_id", "")
        project = Project.objects.get(pk=int(project_id))
        members = Member.objects.filter(project=project)
        return render(request, "projects/exports/grade.html", {'project': project, 'members': members})

    def post(self, request):
        project_id = request.POST.get("id", "")
        project = Project.objects.get(pk=int(project_id))
        score = int(request.POST.get("score"))
        if project and score:
            project_score = Score()
            project_score.score = score
            project_score.expert = request.user
            project_score.project = project
            project_score.save()
            project.p_status = 2
            project.save()
        return redirect(reverse('project_list'))


class DelayView(LoginRequiredMixin, View):
    def get(self, request):
        project_id = request.GET.get("project_id", "")
        project = Project.objects.get(pk=int(project_id))
        return render(request, "projects/students/delay_apply.html", {"project": project})

    def post(self, request):
        project_id = request.POST.get("id", "")
        project = Project.objects.get(pk=int(project_id))
        project.delay_result = request.POST.get("delay_result")
        project.p_status = 7
        project.save()
        return redirect(reverse('project_list'))


class StartMiddleView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.user_type == 1:
            Project.objects.filter(p_status=3).update(p_status=4)
        return redirect(reverse('project_list'))


class MidExamView(LoginRequiredMixin, View):
    def get(self, request):
        project_id = request.GET.get("project_id", "")
        project = Project.objects.get(pk=int(project_id))
        return render(request, "projects/students/mid_exam.html", {"project": project})

    def post(self, request):
        project_id = request.POST.get("id", "")
        project = Project.objects.get(pk=int(project_id))
        middle_form = MiddleForm(request.POST, request.FILES, instance=project)
        if middle_form.is_valid():
            middle_form.save()
        return redirect(reverse('project_list'), kwargs={'msg': "提交中期检查报告成功"})


class LinkView(LoginRequiredMixin, View):
    def post(self, request):
        ids = request.POST.get('ids', '').split(',')
        ids = [int(i) for i in ids]
        group_id = request.POST.get("group_id", "")
        try:
            expert_group = ExpertGroup.objects.get(pk=int(group_id))
            Project.objects.filter(id__in=ids).update(expert_group=expert_group)
            return redirect(reverse('project_list'), kwargs={'msg': "关联成功"})
        except Exception as e:
            return redirect(reverse('project_list'), kwargs={'msg': "关联失败"})


