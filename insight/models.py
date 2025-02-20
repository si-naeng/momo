from mongoengine import Document, EmbeddedDocument, fields, IntField, StringField, DictField


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
    

# Emoticons (Embedded Document)
class Emoticons(EmbeddedDocument):
    weather = fields.StringField()
    emotion = fields.ListField(fields.StringField())  # ✅ 여러 감정 선택 가능
    activity = fields.ListField(fields.StringField())
    daily = fields.ListField(fields.StringField())

# Entries (Embedded Document)
class Entry(EmbeddedDocument):
    date = fields.StringField(required=True)  # 날짜를 문자열로 저장
    emoticons = fields.EmbeddedDocumentField(Emoticons)
    diary = fields.StringField()
    recommend_content = fields.StringField(null=True, default=None)  # ✅ null 허용
    result_emotion = fields.StringField(null=True, default=None)  # ✅ null 허용

# Calendar (Main Document)
class Calendar(Document):
    user_id = fields.StringField(required=True, unique=True)  # ✅ ObjectId 대신 String (Cognito sub 저장)
    mbti = fields.StringField()
    subscribe_platform = fields.StringField()
    entries = fields.MapField(fields.EmbeddedDocumentField(Entry))  # 날짜별 Entry 매핑

    meta = {
        "collection": "calendar",
        "indexes": [
            {"fields": ["user_id"], "unique": True},
        ],
    }

class Contents(Document):
    """
    콘텐츠 정보를 저장하는 모델
    """
    content_id = IntField(required=True, unique=True)  # ID 필드
    title = StringField(required=True)  # Title 필드
    genre = StringField()  # Genre 필드
    platform = StringField()  # Platform 필드
    poster_url = StringField()  # PosterURL 필드
    synopsis = StringField()  # Synopsis 필드
    rating = StringField()  # Rating 필드
    runtime = StringField()  # Runtime 필드
    country = StringField()  # Country 필드
    year = StringField()  # Year 필드
    release_date = StringField()  # ReleaseDate 필드

    meta = {
        'collection': 'contents',  # 컬렉션 이름
        'indexes': [
            'content_id',  # content_id로 인덱스 생성
            'title'  # title로 인덱스 생성
        ]
    }