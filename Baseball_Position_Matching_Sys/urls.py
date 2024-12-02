# Baseball_Position_Matching_Sys/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='baseball_matching/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='baseball_matching:main'), name='logout'),  # 이 부분이 중요합니다
    # Social Auth URLs
    path('accounts/', include('allauth.urls')),
    # App URLs
    path('', include('baseball_matching.urls')),
]