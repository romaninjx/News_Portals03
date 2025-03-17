from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, ArticlesCreate, NewsCreate, ArticlesUpdate, NewsUpdate, PostSearch,
                    error_view, NewsDelete, ArticlesDelete)





urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('<int:pk>', PostDetail.as_view(), name='post_info'),
    path('error/<str:error_name>/<str:error_message>/', error_view, name='error_view'),
    ]