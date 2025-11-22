from django.urls import path
from .views import *

urlpatterns = [
    path('', LevelListView.as_view(), name='levels'),
    path('level/<int:level_number>/', LevelTestView.as_view(), name='level-test'),

    # level crud
    path('levels-crud/', LevelCRUDView.as_view(), name='level-crud'),
    path('levels-crud/edit/<int:level_id>/', LevelCRUDView.as_view(), name='edit-level'),
    path('levels-crud/delete/<int:level_id>/', delete_level, name='delete-level'),
    # admin stats
    path('admin-stats/', AdminTestStatsView.as_view(), name='test_admin_stats'),

    path('quiz/', QuestionAnswerCRUDView.as_view(), name='question-answer-crud'),
    path('quiz/delete-answer/<int:answer_id>/', delete_answer, name='delete-answer'),
    path('quiz/edit/<int:question_id>/', QuestionAnswerCRUDView.as_view(), name='edit-question'),

]
