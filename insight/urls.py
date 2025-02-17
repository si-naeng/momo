from django.urls import path
from .views import *

urlpatterns = [
    path("mbti", MBTIEmotionStatsView.as_view(), name="mbti_emotion_stats"),
]