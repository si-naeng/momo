from mongoengine import Document, EmbeddedDocument, fields, IntField, StringField

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