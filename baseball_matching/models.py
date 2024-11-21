from django.db import models
from django.contrib.auth.models import User

# 데이터베이스 구조를 정의하는 파일
# ORM을 통한 데이터베이스 조작의 기준

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}의 프로필"


class PointHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=[
        ('CHARGE', '충전'),
        ('USE', '사용'),
        ('REFUND', '환불')
    ])
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Game(models.Model):
    GAME_STATUS = [
        ('RECRUITING', '모집중'),
        ('CONFIRMED', '모집완료'),
        ('COMPLETED', '경기완료'),
        ('CANCELED', '취소됨')
    ]

    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    participation_fee = models.IntegerField(default=10000)  # 참가비(포인트)
    max_players_per_team = models.IntegerField(default=9)
    status = models.CharField(max_length=20, choices=GAME_STATUS, default='RECRUITING')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} {self.title}"


class Position(models.Model):
    POSITION_CHOICES = [
        ('P', '투수'),
        ('C', '포수'),
        ('1B', '1루수'),
        ('2B', '2루수'),
        ('3B', '3루수'),
        ('SS', '유격수'),
        ('LF', '좌익수'),
        ('CF', '중견수'),
        ('RF', '우익수'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.CharField(max_length=10, choices=[('HOME', '홈팀'), ('AWAY', '원정팀')])
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    player = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    is_filled = models.BooleanField(default=False)

    class Meta:
        unique_together = ['game', 'team', 'position']

    def __str__(self):
        return f"{self.game.title} - {self.team} {self.get_position_display()}"