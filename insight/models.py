from mongoengine import Document, StringField, DictField, connect


# MongoDB 모델 정의
class ContentMBTIEmotion(Document):
    """
    영화 제목 > MBTI > 감정 > 횟수를 저장하는 MongoDB 모델
    """
    content_title = StringField(required=True, unique=True)  # 영화 제목
    emotion_data = DictField(default=dict)  # 감정 데이터 { MBTI: { 감정: 횟수 } }

    meta = {
        'collection': 'statistics',  # 컬렉션 이름
        'ordering': ['content_title']  # 영화 제목 기준으로 정렬
    }

    def __str__(self):
        return f"MovieTitle: {self.content_title} / Emotions: {self.emotion_data}"


# 데이터 추가 및 업데이트 함수
def add_emotion(content_title, mbti_type, emotion_name):
    """
    주어진 영화 제목에 MBTI와 감정을 추가하거나 업데이트합니다.
    :param content_title: 영화 제목
    :param mbti_type: MBTI 유형 (예: "INTJ")
    :param emotion_name: 감정 이름 (예: "논리적", "감성적")
    """
    # 해당 영화 제목에 대한 문서를 찾거나 새로 생성
    content_data = ContentMBTIEmotion.objects(content_title=content_title).first()
    if not content_data:
        content_data = ContentMBTIEmotion(content_title=content_title)

    # 현재 영화의 감정 데이터 가져오기
    emotion_data = content_data.emotion_data

    # MBTI 유형의 감정 데이터를 초기화 (없으면 추가)
    if mbti_type not in emotion_data:
        emotion_data[mbti_type] = {}

    # 감정 카운트 추가 또는 증가
    if emotion_name in emotion_data[mbti_type]:
        emotion_data[mbti_type][emotion_name] += 1
    else:
        emotion_data[mbti_type][emotion_name] = 1

    # 수정된 데이터를 다시 저장
    content_data.emotion_data = emotion_data
    content_data.save()
    print(f"'{content_title}' 영화의 '{mbti_type}' 유형에 감정 '{emotion_name}' 추가/업데이트 완료.")
