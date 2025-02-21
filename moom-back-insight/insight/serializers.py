from rest_framework_mongoengine import DocumentSerializer
from .models import ContentEmotionStats

class ContentEmotionStatsSerializer(DocumentSerializer):
    class Meta:
        model = ContentEmotionStats
        fields = '__all__'