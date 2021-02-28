from django.urls import path
from . import views

urlpatterns = [
	# path('', views.index, name='index'),
    path('', views.ArtsListView.as_view(), name='art-home'),
    path('art/<int:pk>', views.ArtsDetailView.as_view(), name='art-detail'),
    path('art/new/', views.ArtsCreateView.as_view(), name='art-create'), 
    path('art/category/<str:action>/', views.CategoryView.as_view(), name='art-category'),
]