from django.urls import path
from .views import LevelListView, LevelTestView, AdminTestStatsView

urlpatterns = [
    path('', LevelListView.as_view(), name='levels'),
    path('level/<int:level_number>/', LevelTestView.as_view(), name='level-test'),
    # admin stats
    path('admin-stats/', AdminTestStatsView.as_view(), name='test_admin_stats'),
]
