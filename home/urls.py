from django.urls import path
from .views import *

urlpatterns = [
    path("calendar/read", CalendarReadView.as_view(), name="calendar_list"),
    path("calendar/write", CalendarWriteView.as_view(), name="calendar_write"),
    path("calendar/delete/<str:date>", CalendarDeleteView.as_view(), name="calendar_delete"),
    path("calendar/monthread/<str:year_month>/", CalendarMonthReadView.as_view(), name="calendar_month_read"),
    path("calendar/detail_read/<str:date>", CalendarDetailReadView.as_view(), name="calendar_detail"),
    path("bedrock/<str:date>", CallBedrockForDate.as_view(), name="bedrock_call"),
]


