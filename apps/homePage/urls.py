from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *

urlpatterns = [
  # path("add/user/", AddUserView.as_view(),  name="add-user"),
  # GAME
  path("", Main.as_view(),  name="main"),
  path("home/main/", HomeMainView.as_view(),  name="home"),
  path("start/game/", StartGameView.as_view(),  name="start_game"),
  path("settings/", SettingsGameView.as_view(),  name="settings_game"),
  path('verify-country-code/', verify_country_code, name='verify_country_code'),

  # GLAVNIY
  path('home/main/names_of_allah/', NamesOfAllahView.as_view(), name='names-of-allah'),
  path('home/main/names_of_allah_audio/', AudioListView.as_view(), name='names-of-allah-audio'),

  #PROFILE
  path('home/profile/', ProfileView.as_view(), name='profile'),
  path('home/profile/administration_page/', AdministrationPageView.as_view(), name='administration-page'),
  path('home/profile/administration_page/audio-add/', AudioAddPageView.as_view(), name='administration-page_audio-add'),
  path("audio/<str:action>/", AudioAddPageView.as_view(), name="audio-action"),
  path("audio/<str:action>/<int:pk>/", AudioAddPageView.as_view(), name="audio-action-pk"),

  # path('logout/', LogoutView.as_view(), name="logout"),
  # path('users/list/', ControlUsersView.as_view(), name="control-users"),
  # path('instagram/login/', AccountInstagramView.as_view(), name="account-users"),
  # path('users/change/password/<int:pk>/', EditUserView.as_view(), name="password_change"),
  # path('not_allowed/', NoPermissionsView.as_view(), name="no_permission_page"),
  # path('subscribe_user/', SaveSubscriptionView.as_view(), name="no_permission_page"),
]