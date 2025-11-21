from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *

urlpatterns = [

  path("", ReportGroupView.as_view(),  name="report-group"),
 ]