from django.apps import AppConfig
# Django 애플리케이션의 설정을 담당
# 앱의 구성과 관련된 클래스를 정의

class BaseballMatchingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baseball_matching'

    def ready(self):
        import baseball_matching.signals