from django.conf.urls import url
from .views import LoginView, LogoutView, RegisterView, ExportListView, ExportView, ExportGroupListView, \
    ExportGroupView, ExportGroupAddView, ExportGroupDeleteView, ExportGroupEditView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^export/list/get', ExportListView.as_view()),
    url(r'^export/list/', ExportView.as_view(), name="export_list"),
    url(r'^export/group/list/get', ExportGroupListView.as_view()),
    url(r'^export/group/add', ExportGroupAddView.as_view()),
    url(r'^export/group/delete', ExportGroupDeleteView.as_view()),
    url(r'^export/group/edit', ExportGroupEditView.as_view(), name="export_edit"),
    url(r'^export/group/list/', ExportGroupView.as_view(), name="export_group_list"),
]