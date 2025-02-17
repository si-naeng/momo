import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import ContentEmotionStats

import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import ContentEmotionStats
import matplotlib.font_manager as fm

class MBTIEmotionStatsView(APIView):
    """
    MBTI별 감정 통계를 시각화하여 반환하는 뷰
    """

    def get(self, request):
        # 한글 폰트 설정
        font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 경우
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())

        # 모든 ContentEmotionStats 문서 가져오기
        stats = ContentEmotionStats.objects.all()

        # MBTI별 감정 통계 집계
        mbti_emotion_counts = {}
        for stat in stats:
            for mbti, emotions in stat.mbti_emotions.items():
                if mbti not in mbti_emotion_counts:
                    mbti_emotion_counts[mbti] = {}
                for emotion, count in emotions.items():
                    if emotion in mbti_emotion_counts[mbti]:
                        mbti_emotion_counts[mbti][emotion] += count
                    else:
                        mbti_emotion_counts[mbti][emotion] = count

        # 시각화 생성
        fig, ax = plt.subplots(figsize=(10, 6))
        for mbti, emotions in mbti_emotion_counts.items():
            ax.bar(emotions.keys(), emotions.values(), label=mbti)

        ax.set_xlabel('Emotions', fontproperties=font_prop)
        ax.set_ylabel('Counts', fontproperties=font_prop)
        ax.set_title('MBTI Emotion Statistics', fontproperties=font_prop)
        ax.legend(title='MBTI Types', prop=font_prop)

        # 이미지로 변환
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        return HttpResponse(buf, content_type='image/png')