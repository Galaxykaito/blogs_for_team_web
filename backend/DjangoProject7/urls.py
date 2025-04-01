from django.urls import path
from articles import views

urlpatterns = [
    path('api/member/<int:member_id>/content/', views.member_content),
    path('api/article/<str:identifier>/', views.article_detail),
]