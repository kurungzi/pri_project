# baseball_matching/forms.py

from django import forms
from .models import UserProfile, Game, UsedItem


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



class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_image']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '전화번호를 입력하세요'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'})
        }

class UsedItemForm(forms.ModelForm):
    class Meta:
        model = UsedItem
        fields = ['image','category', 'brand', 'title', 'price', 'condition', 'item_type', 'description']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '카테고리를 입력해주세요'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '브랜드를 입력해주세요'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력해주세요'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '가격을 입력해주세요'
            }),
            'condition': forms.RadioSelect(attrs={
                'class': 'form-check-input d-inline-block'
            }),
            'item_type': forms.RadioSelect(attrs={
                'class': 'form-check-input d-inline-block'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력해 주세요.',
                'rows': 5
            }),

        }

        labels = {
            'image': '이미지',
            'category': '카테고리',
            'brand': '브랜드',
            'title': '제목',
            'price': '가격',
            'condition': '상품상태',
            'item_type': '상품분류',
            'description': '내용',

        }