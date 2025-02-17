from django.urls import path
from .views import *

urlpatterns = [
    path("all/<str:date>", CallBedrockAllPlatform.as_view(), name="bedrock_call_all"),
    path("sub/<str:date>", CallBedrockSubPlatform.as_view(), name="bedrock_call_sub"),
    path("chatbot", QuestionView.as_view(), name="bedrock_chatbot"),
    path("response/<str:date>",BedrockResponseView.as_view(),name="calendar_recommend"),
    path("recommend_content/<str:date>", RecommendContentView.as_view(), name="calendar_recommend"),
]