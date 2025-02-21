from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
import matplotlib.pyplot as plt
import seaborn as sns
import io
from collections import defaultdict
from .models import ContentEmotionStats
from collections import Counter
from .models import *
from datetime import datetime

# Windows
class MBTIEmotionStatsView(APIView):
    """
    View to visualize and return MBTI emotion statistics
    """

    def get(self, request):
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        import io
        from django.http import HttpResponse
        import seaborn as sns

        # 한글 폰트 설정
        font_path = r"C:\Windows\Fonts\malgun.ttf"  # Windows의 경우
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
        sns.set(style="whitegrid")  # 스타일 설정

        fig, ax = plt.subplots(figsize=(12, 8))
        colors = sns.color_palette("husl", len(mbti_emotion_counts))  # 색상 팔레트 설정

        for idx, (mbti, emotions) in enumerate(mbti_emotion_counts.items()):
            ax.bar(emotions.keys(), emotions.values(), label=mbti, color=colors[idx])

        ax.set_xlabel('Emotions', fontproperties=font_prop)
        ax.set_ylabel('Counts', fontproperties=font_prop)
        ax.set_title('MBTI Emotion Statistics', fontproperties=font_prop)
        ax.legend(title='MBTI Types', prop=font_prop)

        # 이미지로 변환
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')  # 그래프가 잘리지 않도록 설정
        plt.close(fig)
        buf.seek(0)

        return HttpResponse(buf, content_type='image/png')

class MBTIRecommendTop5ContentsView(APIView):
    """
    View to return top 5 recommended contents by MBTI
    """

    def get(self, request):
        top_5_recommendations_by_mbti = self.get_top_5_recommendations_by_mbti()

        # 결과를 JSON 형식으로 변환
        result = {
            mbti: [{"title": title, "poster_url": poster_url} for title, poster_url in recommendations]
            for mbti, recommendations in top_5_recommendations_by_mbti.items()
        }

        return JsonResponse(result, safe=False)

    def get_top_5_recommendations_by_mbti(self):
        # 모든 캘린더 문서 가져오기
        all_calendars = Calendar.objects.all()

        # MBTI별 추천 콘텐츠 카운트 저장
        mbti_recommend_count = defaultdict(lambda: defaultdict(int))

        for calendar in all_calendars:
            mbti = calendar.mbti
            for entry in calendar.entries.values():
                if entry.recommend_content:
                    mbti_recommend_count[mbti][entry.recommend_content] += 1

        # MBTI별 추천 콘텐츠 상위 5개 추출
        top_5_recommendations_by_mbti = {}
        for mbti, recommend_count in mbti_recommend_count.items():
            top_5_recommendations = sorted(recommend_count.items(), key=lambda x: x[1], reverse=True)[:5]

            # 콘텐츠 정보 가져오기
            top_5_contents = []
            for title, _ in top_5_recommendations:
                content = Contents.objects(title=title).first()
                if content:
                    top_5_contents.append((content.title, content.poster_url))

            top_5_recommendations_by_mbti[mbti] = top_5_contents

        return top_5_recommendations_by_mbti

class MBTIMemberCountView(APIView):
    """
    View to visualize and return member count by MBTI
    """

    def get(self, request):
        # 모든 캘린더 문서 가져오기
        all_calendars = Calendar.objects.all()

        # MBTI별 회원 수 집계
        mbti_counts = Counter(calendar.mbti for calendar in all_calendars if calendar.mbti)

        # 시각화 생성
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 6))
        mbti_types = list(mbti_counts.keys())
        counts = list(mbti_counts.values())
        ax.bar(mbti_types, counts, color=sns.color_palette("husl", len(mbti_types)))

        ax.set_xlabel('MBTI Type')
        ax.set_ylabel('Member Count')
        ax.set_title('Member Count by MBTI')

        # 이미지로 변환
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)

        return HttpResponse(buf, content_type='image/png')

class EmotionTop5ContentsView(APIView):
    """
    View to visualize and return top 5
     movies by emotion
    """

    def get(self, request):
        top_5_movies = self.get_top_5_movies_by_emotion()

        # 결과를 JSON 형식으로 변환
        result = {
            emotion: [{"title": title, "poster_url": poster_url} for title, _, poster_url in movies]
            for emotion, movies in top_5_movies.items()
        }

        return JsonResponse(result, safe=False)

    def get_top_5_movies_by_emotion(self):
        # 모든 문서 가져오기
        all_stats = ContentEmotionStats.objects.all()

        # 감정별 영화 감정 합산 저장
        emotion_movie_scores = defaultdict(list)

        for stat in all_stats:
            for mbti, emotions in stat.mbti_emotions.items():
                for emotion, count in emotions.items():
                    # (영화 제목, 감정 카운트, 포스터 URL) 튜플 추가
                    emotion_movie_scores[emotion].append((stat.title, count, stat.poster_url))

        # 감정별 상위 5개 영화 추출
        top_5_movies_by_emotion = {}
        for emotion, movies in emotion_movie_scores.items():
            # 감정 카운트를 기준으로 정렬 후 상위 5개 선택
            top_5_movies_by_emotion[emotion] = sorted(movies, key=lambda x: x[1], reverse=True)[:5]

        return top_5_movies_by_emotion

class TodayEmotionTop5ContentsView(APIView):
    """
    View to visualize and return top 5 movies by emotion for today
    """

    def get(self, request):
        try:
            # 오늘 날짜 가져오기
            today = datetime.now().strftime('%Y-%m-%d')

            # 오늘의 감정 데이터 수집
            emotion_counts = self.collect_today_emotions(today)

            # 감정별 상위 5개 영화 추출
            top_5_movies = self.get_top_5_movies_by_emotion(emotion_counts)

            if not top_5_movies:
                return JsonResponse({'message': 'No data available for today\'s emotions.'}, status=200)

            # 시각화 설정
            sns.set(style="whitegrid")
            fig, axes = plt.subplots(nrows=len(top_5_movies), ncols=1, figsize=(10, 5 * len(top_5_movies)))

            if len(top_5_movies) == 1:
                axes = [axes]  # 단일 플롯일 경우 리스트로 변환

            for ax, (emotion, movies) in zip(axes, top_5_movies.items()):
                titles = [title for title, _ in movies]
                scores = [score for _, score in movies]
                ax.bar(titles, scores, color=sns.color_palette("husl", len(titles)))
                ax.set_title(f"Top 5 Movies for Emotion: {emotion} on {today}")
                ax.set_xlabel("Movie Title")
                ax.set_ylabel("Total Emotion Count")

            plt.tight_layout()

            # 이미지로 변환
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            plt.close(fig)
            buf.seek(0)

            return HttpResponse(buf, content_type='image/png')

        except Exception as e:
            # 예외 발생 시 오류 메시지 반환
            return JsonResponse({'error': str(e)}, status=500)

    def collect_today_emotions(self, target_date):
        # 모든 캘린더 문서 가져오기
        all_calendars = Calendar.objects.all()

        # 오늘의 감정 데이터 수집
        emotion_counts = Counter()

        for calendar in all_calendars:
            entry = calendar.entries.get(target_date)
            if entry and entry.emoticons:
                for emotion in entry.emoticons.emotion:
                    emotion_counts[emotion] += 1

        return emotion_counts

    def get_top_5_movies_by_emotion(self, emotion_counts):
        # 감정별 영화 감정 합산 저장
        emotion_movie_scores = defaultdict(list)

        # 모든 문서 가져오기
        all_stats = ContentEmotionStats.objects.all()

        for stat in all_stats:
            for mbti, emotions in stat.mbti_emotions.items():
                for emotion, count in emotions.items():
                    if emotion in emotion_counts:
                        # (영화 제목, 감정 카운트) 튜플 추가
                        emotion_movie_scores[emotion].append((stat.title, count))

        # 감정별 상위 5개 영화 추출
        top_5_movies_by_emotion = {}
        for emotion, movies in emotion_movie_scores.items():
            # 감정 카운트를 기준으로 정렬 후 상위 5개 선택
            top_5_movies_by_emotion[emotion] = sorted(movies, key=lambda x: x[1], reverse=True)[:5]

        return top_5_movies_by_emotion