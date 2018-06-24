import json
from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Notice, NoticeResource


class ListView(View):
    def get(self, request):
        notices = Notice.objects.filter(end_time__gte=datetime.now()).order_by('end_time')
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            notices = notices.filter(name__icontains=search_keywords)
        return_data = {"total": notices.count(), "rows": []}
        for notice in notices:
            return_data['rows'].append({
                'id': notice.id,
                'name': notice.name,
                'type': notice.get_type_display(),
                'end_time': notice.end_time.strftime('%Y-%m-%d')
            })
        return HttpResponse(json.dumps(return_data), content_type='application/json')


class NoticesView(View):
    def get(self, request):
        return render(request, 'notices/list.html')


class NoticeDetalView(LoginRequiredMixin, View):
    def get(self, request):
        notice_id = request.GET.get('notice_id', "")
        notice = Notice.objects.get(pk=notice_id)
        resources = NoticeResource.objects.filter(notice=notice)
        return render(request, 'notices/detal.html', {'notice': notice, 'resources': resources})
