from django.contrib import admin
from .models import UserProfile, Game, Position, PointHistory

#Django 관리자 인터페이스를 구성하는 파일
#모델을 관리자 페이지에 등록하고 커스터마이징하는 역할

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Position)
admin.site.register(PointHistory)