from mongoengine import Document, EmbeddedDocument, fields

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
    recommend_content = fields.ObjectIdField(null=True, default=None)  # ✅ null 허용
    result_emotion = fields.StringField(null=True, default=None)  # ✅ null 허용

# Calendar (Main Document)
class Calendar(Document):
    user_id = fields.StringField(required=True, unique=True)  # ✅ ObjectId 대신 String (Cognito sub 저장)
    mbti = fields.StringField()
    entries = fields.MapField(fields.EmbeddedDocumentField(Entry))  # 날짜별 Entry 매핑

    meta = {
        "collection": "calendar",
        "indexes": [
            {"fields": ["user_id"], "unique": True},
        ],
    }