from bson import ObjectId
from mongoengine import Document, StringField, EmailField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
    nickname = StringField(required=True, max_length=50)  # 추가 예시
    created_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


