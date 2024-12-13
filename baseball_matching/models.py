from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 데이터베이스 구조를 정의하는 파일
# ORM을 통한 데이터베이스 조작의 기준

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return '/static/images/baseball_user_image.webp'

    def get_participation_count(self):
        # 사용자의 총 경기 참여 횟수를 계산
        return Position.objects.filter(
            player=self,
            is_filled=True
        ).count()

    def get_level(self):
        participation_count = self.get_participation_count()

        if participation_count >= 100:
            return 8
        elif participation_count >= 60:
            return 7
        elif participation_count >= 40:
            return 6
        elif participation_count >= 20:
            return 5
        elif participation_count >= 12:
            return 4
        elif participation_count >= 6:
            return 3
        elif participation_count >= 2:
            return 2
        else:
            return 1

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

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
    creator = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='created_games',
        null=True,  # null 허용
        blank=True  # 폼에서 비워둘 수 있음
    )

    def __str__(self):
        return f"{self.date} {self.title}"

class ChatRoom(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_chats')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer_chats')
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


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


class UsedItem(models.Model):
    CONDITION_CHOICES = [
        ('상', '상'),
        ('중', '중'),
        ('하', '하')
    ]
    ITEM_TYPE_CHOICES = [
        ('중고', '중고'),
        ('신제품', '신제품')
    ]

    STATUS_CHOICES = [
        ('판매중', '판매중'),
        ('예약중', '예약중'),
        ('거래완료', '거래완료')
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='판매중'
    )

    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    category = models.CharField(max_length=100)  # 배트, 글러브 등
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='used_items/')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)