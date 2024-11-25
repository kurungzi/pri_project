# baseball_matching/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Game, Position, PointHistory

# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')

# Game Admin
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'status', 'participation_fee')
    list_filter = ('status', 'date')
    search_fields = ('title', 'location')

# Position Admin
class PositionAdmin(admin.ModelAdmin):
    list_display = ('game', 'team', 'position', 'player', 'is_filled')
    list_filter = ('team', 'position', 'is_filled')
    search_fields = ('game__title', 'player__user__username')

# PointHistory Admin
class PointHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__user__username', 'description')

# Register models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(PointHistory, PointHistoryAdmin)