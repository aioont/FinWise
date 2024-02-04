from django.urls import path
from .views import article_list, article_detail
#, user_learning_path, edit_learning_path

urlpatterns = [
    path('articles/', article_list, name='article_list'),
    path('articles/<int:article_id>/', article_detail, name='article_detail'),
    # path('learning-path/', user_learning_path, name='user_learning_path'),
    # path('learning-path/edit/', edit_learning_path, name='edit_learning_path'),
]
