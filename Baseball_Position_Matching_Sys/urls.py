# Baseball_Position_Matching_Sys/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


#
# # GET 요청도 허용하는 커스텀 LogoutView 생성
# class CustomLogoutView(auth_views.LogoutView):
#     http_method_names = ['get', 'post']
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/login/', auth_views.LoginView.as_view(template_name='baseball_matching/login.html'), name='login'),
#     path('accounts/logout/', CustomLogoutView.as_view(next_page='baseball_matching:game_list'), name='logout'),
#     path('', include('baseball_matching.urls')),
# ]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # allauth URLs
#     path('accounts/', include('allauth.urls')),
#     # 기존 로그인/로그아웃 URL
#     path('accounts/login/', auth_views.LoginView.as_view(template_name='baseball_matching/login.html'), name='login'),
#     path('accounts/logout/', auth_views.LogoutView.as_view(next_page='baseball_matching:main'), name='logout'),
#     # baseball_matching URLs
#     path('', include('baseball_matching.urls')),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='baseball_matching/login.html',  # 이 부분이 중요합니다
    ), name='login'),
    path('accounts/', include('allauth.urls')),
    path('', include('baseball_matching.urls')),
]