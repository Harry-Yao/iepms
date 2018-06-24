from django.conf.urls import url
from .views import ListView, NoticesView, NoticeDetalView

urlpatterns = [
    url(r'^list/get', ListView.as_view()),
    url(r'^list/', NoticesView.as_view(), name="notice_list"),
    url(r'^detal/$', NoticeDetalView.as_view(), name="notice_detal"),
]