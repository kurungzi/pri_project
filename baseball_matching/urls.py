# baseball_matching/urls.py
from django.urls import path
from . import views

# URL 패턴과 뷰를 매핑하는 파일
# 웹 애플리케이션의 라우팅을 담당

app_name = 'baseball_matching'

urlpatterns = [
    path('', views.main, name='main'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('games/create/', views.game_create, name='game_create'),
    path('position/<int:position_id>/join/', views.join_position, name='join_position'),
    path('position/<int:position_id>/cancel/', views.cancel_position, name='cancel_position'),
    path('points/charge/', views.charge_points, name='charge_points'),
    path('points/history/', views.point_history, name='point_history'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('used-items/', views.used_item_list, name='used_item_list'),
    path('used-items/create/', views.used_item_create, name='used_item_create'),
    path('used-items/<int:item_id>/', views.used_item_detail, name='used_item_detail'),
    path('used-items/<int:item_id>/', views.used_item_detail, name='used_item_detail'),
    path('chat/<int:seller_id>/', views.chat_room, name='chat_room'),
    path('used-items/<int:item_id>/change-status/', views.change_item_status, name='change_item_status'),
    path('games/<int:game_id>/edit/', views.game_edit, name='game_edit'),
    path('games/<int:game_id>/delete/', views.game_delete, name='game_delete'),
    path('used-items/<int:item_id>/edit/', views.used_item_edit, name='used_item_edit'),
    path('used-items/<int:item_id>/delete/', views.used_item_delete, name='used_item_delete'),
]