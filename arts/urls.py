from django.urls import path
from . import views

urlpatterns = [
	# path('', views.index, name='index'),
    path('', views.ArtsListView.as_view(), name='art-home'),
    path('art/<int:pk>', views.ArtsDetailView.as_view(), name='art-detail'),
    path('art/new/', views.ArtsCreateView.as_view(), name='art-create'), 
    path('art/category/<str:action>/', views.CategoryView.as_view(), name='art-category'),
    path('art/<int:pk>/delete/', views.ArtsDeleteView.as_view(), name = 'art-delete'), 
    # 自分の投稿一覧を拾う
    path('art/mylist/', views.MyArtView.as_view(), name='art-mylist'),
    #いいね機能のため追加
    path('art/like', views.LikeView, name='like'),
    #いいねした投稿一覧を拾う
    path('art/mylike/', views.MyLikeView.as_view(), name='art-mylike'),
]