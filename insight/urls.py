from django.urls import path
from .views import *

urlpatterns = [
    path("mbti_all", MBTIEmotionStatsView.as_view(), name="mbti_emotion_stats"),
    path("mbti_top5_contents", MBTITop5View.as_view(), name="mbti_emotion_chart"),
    path("mbti_member", MBTIMemberCountView.as_view(), name="mbti_emotion_chart"),
    path("emotion_top5", EmotionTop5ContentsView.as_view(), name="mbti_emotion_chart"),
    path("today_top5_emotion", TodayEmotionTop5ContentsView.as_view(), name="mbti_emotion_chart"),
]