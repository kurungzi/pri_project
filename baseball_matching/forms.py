# baseball_matching/forms.py

from django import forms
from .models import Game, UserProfile

from django import forms
from .models import Game

# 웹 폼을 정의하고 유효성 검사를 처리
# 모델 폼과 일반 폼을 정의

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'date', 'time', 'location', 'participation_fee', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '경기 제목을 입력하세요'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '경기 장소를 입력하세요'
            }),
            'participation_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1000',
                'placeholder': '참가비를 입력하세요'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '경기에 대한 설명을 입력하세요'
            }),
        }
        labels = {
            'title': '경기 제목',
            'date': '날짜',
            'time': '시간',
            'location': '장소',
            'participation_fee': '참가비 (포인트)',
            'description': '설명',
        }

# class GameForm(forms.ModelForm):
#     class Meta:
#         model = Game
#         fields = ['title', 'date', 'time', 'location', 'participation_fee', 'description']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'location': forms.TextInput(attrs={'class': 'form-control'}),
#             'participation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#         }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '전화번호를 입력하세요'
            })
        }