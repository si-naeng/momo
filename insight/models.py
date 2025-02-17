from mongoengine import Document, StringField, DictField


class ContentEmotionStats(Document):
    """
    콘텐츠별 MBTI 감정 통계를 저장하는 모델

    구조:
    {
        "title": "영화제목",
        "mbti_emotions": {
            "ENFP": {
                "기쁨": 3,
                "슬픔": 1,
                "분노": 2
            },
            "INTJ": {
                "기쁨": 1,
                "불안": 2
            }
        }
    }
    """
    title = StringField(required=True, unique=True)
    mbti_emotions = DictField(default={})  # MBTI별 감정 카운트를 저장

    meta = {
        'collection': 'content_emotion_stats',
        'indexes': [
            'title'
        ]
    }

    def add_emotions(self, mbti: str, emotions: list):
        """
        특정 MBTI 유형의 감정들을 추가하거나 카운트를 증가시킵니다.

        :param mbti: MBTI 유형 (예: "ENFP")
        :param emotions: 감정 리스트 (예: ["기쁨", "슬픔"])
        """
        # MBTI가 없으면 초기화
        if mbti not in self.mbti_emotions:
            self.mbti_emotions[mbti] = {}

        # 각 감정에 대해 카운트 증가
        for emotion in emotions:
            if emotion in self.mbti_emotions[mbti]:
                self.mbti_emotions[mbti][emotion] += 1
            else:
                self.mbti_emotions[mbti][emotion] = 1

        self.save()

    def get_mbti_emotions(self, mbti: str = None):
        """
        특정 MBTI 유형 또는 전체 MBTI 유형의 감정 통계를 조회합니다.

        :param mbti: MBTI 유형 (None인 경우 전체 데이터 반환)
        :return: 감정 통계 데이터
        """
        if mbti:
            return self.mbti_emotions.get(mbti, {})
        return self.mbti_emotions

    def get_emotion_count(self, mbti: str, emotion: str):
        """
        특정 MBTI 유형의 특정 감정 카운트를 조회합니다.

        :param mbti: MBTI 유형
        :param emotion: 감정
        :return: 감정 카운트 (없으면 0 반환)
        """
        return self.mbti_emotions.get(mbti, {}).get(emotion, 0)