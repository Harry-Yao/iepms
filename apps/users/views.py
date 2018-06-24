import json
from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import LoginForm, RegisterForm
from .models import UserProfile, ExpertGroup


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "base.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    msg = "登录失败"
            else:
                msg = "用户或密码错误或用户未激活"
        else:
            msg = "登录失败"
        return render(request, "login.html", {
            'msg': msg,
            'login_form': login_form
        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("username", "")
            user_type = request.POST.get("type", "")
            college = request.POST.get("college", "")
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            re_passwrod = request.POST.get("re_password", "")
            if UserProfile.objects.filter(username=username):
                return render(request, "register.html", {
                    'msg': "用户已存在",
                    'register_form': register_form
                })
            elif password != re_passwrod:
                return render(request, "register.html", {
                    'msg': "两次密码输入不一致",
                    'register_form': register_form
                })
            else:
                password = request.POST.get("password", "")
                user = UserProfile()
                user.username = username
                user.user_type = user_type
                user.college = college
                user.email = email
                user.password = make_password(password)
                user.is_active = True
                user.save()
                return render(request, "login.html", {
                    'msg': "注册成功！请登录"
                })
        else:
            return render(request, "register.html", {'register_form': register_form})


class ExportView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "projects/managements/expert_list.html")
    

class ExportListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        search_keywords = request.GET.get('college', "")
        exports = UserProfile.objects.filter(user_type=2)
        if search_keywords:
            exports = exports.filter(college=int(search_keywords))
        if not offset:
            offset = 0
        if not limit:
            limit = 10  # 默认是每页20行的内容，与前端默认行数一致
        if exports:
            pageinator = Paginator(exports, int(limit))
            page = int(int(offset) / int(limit) + 1)

            return_data = {"total": "", "rows": []}
            if exports.count():
                return_data['total'] = exports.count()

            for export in pageinator.page(page):
                group_name = None
                if export.expert_group:
                    group_name = export.expert_group.name
                return_data['rows'].append({
                    'id': export.id,
                    'username': export.username,
                    'college': export.get_college_display(),
                    'expert_group': group_name,
                })
            return HttpResponse(json.dumps(return_data), content_type='application/json')

    def post(self, request):
        college = (
            (0, '电子信息学院'),
            (1, '机电工程学院'),
            (2, '计算机学院'),
            (3, '材料与食品学院'),
            (4, '人文社会科学学院'),
            (5, '管理学院'),
            (6, '经贸学院'),
            (7, '外国语学院'),
            (8, '艺术设计学院')
        )
        exports = UserProfile.objects.filter(user_type=2)
        results = []
        for c in college:
            college_exports = exports.filter(user_type=2, college=c[0])
            group = {'text': c[1], 'children': ''}
            export_list = [{'id': export.id, 'text': export.username} for export in college_exports]
            group['children'] = export_list
            results.append(group)
        return_data = {
            'results': results
        }
        return HttpResponse(json.dumps(return_data), content_type='application/json')


class ExportGroupView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "projects/managements/expert_group_list.html")


class ExportGroupListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        search_keywords = request.GET.get('college', "")
        export_groups = ExpertGroup.objects.all().order_by('id')
        if search_keywords:
            export_groups = export_groups.filter()
        if not offset:
            offset = 0
        if not limit:
            limit = 10  # 默认是每页20行的内容，与前端默认行数一致
        if export_groups:
            pageinator = Paginator(export_groups, int(limit))
            page = int(int(offset) / int(limit) + 1)

            return_data = {"total": "", "rows": []}
            if export_groups.count():
                return_data['total'] = export_groups.count()

            for export_group in pageinator.page(page):
                members = None
                exports = export_group.userprofile_set.all()
                if exports.count != 0:
                    members = [''.join(x.username+"("+x.get_college_display()+") ") for x in exports]
                return_data['rows'].append({
                    'id': export_group.id,
                    'name': export_group.name,
                    'members': members,
                })
            return HttpResponse(json.dumps(return_data), content_type='application/json')

    def post(self, request):
        groups = ExpertGroup.objects.all()
        groups = [{'id': g.id, 'text': g.name} for g in groups]
        return_data = {
            'results': groups
        }
        return HttpResponse(json.dumps(return_data), content_type='application/json')


class ExportGroupAddView(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get('group_name')
        group = ExpertGroup()
        group.name = name
        result = group.save()
        return HttpResponse(json.dumps(result), content_type='application/json')


class ExportGroupDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        ids = request.POST.get('ids').split(',')
        result = [ExpertGroup.objects.filter(id=int(group_id)).delete() for group_id in ids]
        return HttpResponse(json.dumps(result), content_type='application/json')


class ExportGroupEditView(LoginRequiredMixin, View):
    def get(self, request):
        group_id = request.GET.get("group_id", "")
        try:
            expert_group = ExpertGroup.objects.get(pk=int(group_id))
            return render(request, "projects/managements/expert_group_edit.html", {'expert_group': expert_group})
        except Exception as e:
            print(e)
            return redirect(reverse('export_group_list'), kwargs={'msg': "获取出错"})

    def post(self, request):
        group_id = request.POST.get("group_id", "")
        group_name = request.POST.get("group_name", "")
        members = request.POST.get("members", "").split(',')
        members = [int(m) for m in members]
        try:
            expert_group = ExpertGroup.objects.get(pk=int(group_id))
            expert_group.name = group_name
            expert_group.save()
            UserProfile.objects.filter(expert_group=expert_group).update(expert_group=None)
            if members:
                UserProfile.objects.filter(pk__in=members).update(expert_group=expert_group)
            return redirect(reverse('export_group_list'), kwargs={'msg': "编辑成功"})
        except Exception as e:
            print(e)
            return redirect(reverse('export_group_list'), kwargs={'msg': "编辑失败"})
