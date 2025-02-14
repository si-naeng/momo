from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.serializers import *
from .models import Calendar, Entry, Emoticons


class EmoticonsSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Emoticons
        fields = ("weather", "emotion", "activity", "daily")

class EntrySerializer(EmbeddedDocumentSerializer):
    emoticons = EmoticonsSerializer()

    class Meta:
        model = Entry
        fields = ("date", "emoticons", "diary", "result_emotion")

class CalendarSerializer(DocumentSerializer):
    entries = serializers.DictField(child=EntrySerializer())  # 여기를 수정!

    class Meta:
        model = Calendar
        fields = ("user_id", "mbti", "entries")

class DateSerializer(DocumentSerializer):
    class Meta:
        model = Calendar
        fields = ("date",)

class PersonalSerializer(DocumentSerializer):
    class Meta:
        model = Calendar
        fields = ("mbti", "subscribe_platform")

from rest_framework import serializers


class QuestionSerializer(serializers.Serializer):
    question_text = serializers.CharField()

class RecommendSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Entry
        fields = ("recommend_content", "result_emotion")
