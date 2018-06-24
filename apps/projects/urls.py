from django.conf.urls import url
from .views import ProjectsView, ListView, ProjectDetalView,  ApplyView, UpdateView, ApprovalView, GradeView, \
    DelayView, StartMiddleView, MidExamView, LinkView


urlpatterns = [
    url(r'^list/get', ListView.as_view()),
    url(r'^list/', ProjectsView.as_view(), name="project_list"),
    url(r'^detal/', ProjectDetalView.as_view(), name="project_detal"),
    url(r'^apply', ApplyView.as_view(), name="apply"),
    url(r'^update', UpdateView.as_view(), name="update"),
    url(r'^approval', ApprovalView.as_view(), name="approval"),
    url(r'^link', LinkView.as_view(), name="link"),
    url(r'^grade', GradeView.as_view(), name="grade"),
    url(r'^delay', DelayView.as_view(), name="delay"),
    url(r'^mid_exam', MidExamView.as_view(), name="mid_exam"),
    url(r'^start_mid', StartMiddleView.as_view(), name="start_mid"),
]