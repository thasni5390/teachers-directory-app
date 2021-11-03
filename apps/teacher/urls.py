from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    url(r'^list/$', views.TeachersList.as_view(), name='teachers_list'),
    url(r'^bulk-upload/$', views.TeachersBulkUpload.as_view(), name='teachers_bulk_upload'),
    url(r'^detail/(?P<pk>\d+)/$', views.TeacherDetail.as_view(), name='teacher_detail'),
    url(r'^create/$', views.TeacherCreateView.as_view(), name='teacher_create'),
    url(r'^edit/(?P<pk>\d+)$', views.TeacherUpdateView.as_view(), name='teacher_update'),
]
