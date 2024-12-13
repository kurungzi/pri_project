from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from baseball_matching.models import *  # 모든 모델을 import
from rest_framework.test import APITestCase
from django.utils import timezone


class UsedItemAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_used_item_create(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        # 테스트용 이미지 데이터 생성
        image_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
        image = SimpleUploadedFile(
            name='test_image.gif',
            content=image_data,
            content_type='image/gif'
        )

        item_data = {
            'title': '테스트 글러브',
            'price': 50000,
            'condition': '상',
            'description': '테스트 설명',
            'category': '글러브',
            'brand': '윌슨',
            'item_type': '중고',
            'image': image
        }

        response = self.client.post(
            reverse('baseball_matching:used_item_create'),
            item_data,
            format='multipart'
        )

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        print("All UsedItems in DB:", list(UsedItem.objects.all()))

        # response.context가 있을 때만 폼 에러를 출력
        if hasattr(response, 'context') and response.context is not None:
            if 'form' in response.context:
                print("Form errors:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  # 성공 시 리다이렉트
        self.assertTrue(UsedItem.objects.filter(title='테스트 글러브').exists())