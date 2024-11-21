# baseball_matching/urls.py
from django.urls import path
from . import views

# URL 패턴과 뷰를 매핑하는 파일
# 웹 애플리케이션의 라우팅을 담당

app_name = 'baseball_matching'

urlpatterns = [
    # 메인 페이지 (경기 목록)
    path('', views.main, name='main'),
    path('', views.game_list, name='game_list'),

    # 경기 관련 URLs
    path('games/', views.game_list, name='game_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),  # 이 줄 확인
    path('games/create/', views.game_create, name='game_create'),

    # 포지션 신청 관련
    path('position/<int:position_id>/join/', views.join_position, name='join_position'),
    path('position/<int:position_id>/cancel/', views.cancel_position, name='cancel_position'),

    # 포인트 관련 URLs
    path('points/charge/', views.charge_points, name='charge_points'),
    path('points/history/', views.point_history, name='point_history'),

    # 사용자 관련 URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]