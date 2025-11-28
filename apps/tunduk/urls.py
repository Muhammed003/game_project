from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *

urlpatterns = [
  path("start/tun/", pin_view, name="pin"),
  path("main/tun/main/", TunMainView.as_view(), name="tun-main"),
  path("main/documents/list/", DocumentsListView.as_view(), name="tun-documents"),
  path("main/documents/passport/", PassportView.as_view(), name="passport-documents"),
 ]