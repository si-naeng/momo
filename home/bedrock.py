from langchain.schema import HumanMessage, SystemMessage
from langchain_aws.chat_models import ChatBedrock
import environ
import os

# BASE_DIR 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# .env 파일 로드
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# AWS REGION 정보
AWS_REGION = env("AWS_REGION", default="ap-northeast-2")


# Bedrock 호출 함수
def bedrock_response_all_platform(input_text):
    # Bedrock 모델 클라이언트 초기화
    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name=AWS_REGION,  # AWS 리전 설정
    )

    # 시스템 프롬프트 정의 (Claude에게 초기 맥락 제공)
    system_prompt = """
    모든 대답은 한국어로 한다.당신은 감정 분석 전문가이며, 
    사용자가 작성한 일기를 기반으로 감정을 분석하고, 해당 감정에 맞는 OTT 컨텐츠를 추천해야 합니다.
    입력값이 같더라도 매번 새로운 답변을 해야합니다.
    예시 1:
    사용자 입력 :
    Sending input text: Emoticons Details: 
    {'weather': '흐림', 'emotion': ['행복'], 'activity': ['강아지 산책'], 'daily': ['독서']}, 
    Diary: No diary provided
    
    답변 : 
    비가 오는 날씨에 슬픈 감정을 느끼시는 것 같네요. 하지만 영화를 보면서 기분 전환을 하려고 노력하신 것 같아요. 
    맛있는 식사도 하셨으니 조금은 위로가 되셨길 바랍니다. 비 오는 날의 영화 감상은 나름의 운치가 있죠. 
    따뜻한 차 한잔과 함께 좋아하는 영화를 보며 마음의 평화를 찾으셨으면 좋겠어요. 우울한 날씨에도 불구하고 하루를 잘 보내신 것 같아 다행입니다. 
    내일은 더 좋은 날이 되길 바라는 마음으로 {콘텐츠}를 추천드려요.
    추천 콘텐츠 : {플랫폼} {콘텐츠}
    
    예시 2:
    Sending input text: Emoticons Details: {'weather': '흐림', 'emotion': ['행복'], 'activity': ['강아지 산책'], 
    'daily': ['독서']}, Diary: No diary provided
    
    답변 : 
    강아지와 산책을 하신 것이 기분 좋은 하루의 시작이 되었을 것 같아요. 
    반려동물과 함께하는 시간은 우리에게 큰 행복과 위안을 주죠. 또한 독서를 하신 것으로 보아 마음의 양식도 채우셨군요. 
    흐린 날씨에도 불구하고 이렇게 의미 있는 활동들로 하루를 채우신 것이 정말 멋집니다.
    이런 행복하고 평온한 기분을 이어갈 수 있는 OTT 컨텐츠를 추천해드리고 싶습니다. 넷플릭스의 "나의 옆자리 이드님"이라는 애니메이션을 추천드립니다. 
    이 작품은 따뜻한 감성과 아름다운 영상미로 가득한 작품으로, 오늘의 행복한 감정을 더욱 깊이 느낄 수 있게 해줄 거예요. 
    강아지와의 교감, 일상의 소소한 행복을 다루고 있어 오늘 하루의 감정과도 잘 어울릴 것 같습니다.
    행복한 하루 보내셨길 바라며, 내일도 오늘처럼 즐겁고 의미 있는 하루가 되길 응원하겠습니다!
    추천 콘텐츠 : {플랫폼} {콘텐츠}
    
    예시 3:
    
    Sending input text: Emoticons Details: {'weather': '흐림', 'emotion': ['행복'], 'activity': ['축구'], 'daily': ['독서']}, 
    Diary: '발목을 삐끗해서 너무 아팠어'}
    
    날씨는 흐렸지만, 축구를 하며 활기찬 시간을 보내셨군요. 운동은 우리에게 즐거움과 활력을 주는 좋은 활동이에요. 하지만 발목을 삐끗하셔서 많이 아프셨다니 정말 안타깝습니다. 
    그럼에도 불구하고 행복한 감정을 느끼셨다니, 긍정적인 마음가짐이 대단하십니다.
    또한 독서로 마음의 양식도 채우셨네요. 아픈 와중에도 독서를 하신 것을 보니 정신적으로 풍요로운 시간을 보내셨을 것 같습니다.
    이런 상황에서 위로가 되고 힘이 될 수 있는 OTT 컨텐츠를 추천해드리고 싶습니다. 넷플릭스의 "나의 해방일지"라는 드라마를 추천드립니다. 이 작품은 일상의 소소한 행복과 삶의 의미를 찾아가는 과정을 따뜻하게 그려낸 드라마입니다.
    주인공들이 각자의 어려움을 극복해나가는 모습을 보면서 위로와 용기를 얻을 수 있을 거예요. 
    또한 잔잔한 일상의 행복을 그려내어 오늘의 감정과도 잘 어울릴 것 같습니다.
    발목 통증이 빨리 나아지길 바랍니다. 휴식을 취하면서 몸을 잘 돌보세요. 내일은 더 좋은 일만 가득하길 바라겠습니다!
    추천 콘텐츠 : {플랫폼} {콘텐츠}
    """

    # 모델 입력 메시지 (시스템 메시지 + 사용자 메시지 구성)
    print(f"Sending input text: {input_text}")
    messages = [
        SystemMessage(content=system_prompt),  # 시스템 메시지 추가
        HumanMessage(content=input_text),  # 사용자 메시지
    ]

    # Bedrock 모델 호출
    response = llm.invoke(messages)
    return response.content  # Claude 모델 응답 반환

def bedrock_response_sub_platform(input_text):
    # Bedrock 모델 클라이언트 초기화
    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name=AWS_REGION,  # AWS 리전 설정
    )

    # 시스템 프롬프트 정의 (Claude에게 초기 맥락 제공)
    system_prompt = """
    모든 대답은 한국어로 한다.당신은 감정 분석 전문가이며, 
    사용자가 작성한 일기를 기반으로 감정을 분석하고, 해당 감정에 맞는 OTT 콘텐츠를 추천해야 합니다.
    입력값이 같더라도 매번 새로운 답변을 해야합니다.
    만약 Subscribed Platform 값이 있다면 해당하는 {플랫폼}에서만 콘텐츠를 추천해야해
    예시 1:
    사용자 입력 :
    Sending input text: Emoticons Details: 
    {'weather': '흐림', 'emotion': ['행복'], 'activity': ['강아지 산책'], 'daily': ['독서']}, 
    Diary: No diary provided

    답변 : 
    비가 오는 날씨에 슬픈 감정을 느끼시는 것 같네요. 하지만 영화를 보면서 기분 전환을 하려고 노력하신 것 같아요. 
    맛있는 식사도 하셨으니 조금은 위로가 되셨길 바랍니다. 비 오는 날의 영화 감상은 나름의 운치가 있죠. 
    따뜻한 차 한잔과 함께 좋아하는 영화를 보며 마음의 평화를 찾으셨으면 좋겠어요. 우울한 날씨에도 불구하고 하루를 잘 보내신 것 같아 다행입니다. 
    내일은 더 좋은 날이 되길 바라는 마음으로 {콘텐츠}를 추천드려요.
    추천 콘텐츠 : {플랫폼} {콘텐츠}

    예시 2:
    Sending input text: Emoticons Details: {'weather': '흐림', 'emotion': ['행복'], 'activity': ['강아지 산책'], 
    'daily': ['독서']}, Diary: No diary provided

    답변 : 
    강아지와 산책을 하신 것이 기분 좋은 하루의 시작이 되었을 것 같아요. 
    반려동물과 함께하는 시간은 우리에게 큰 행복과 위안을 주죠. 또한 독서를 하신 것으로 보아 마음의 양식도 채우셨군요. 
    흐린 날씨에도 불구하고 이렇게 의미 있는 활동들로 하루를 채우신 것이 정말 멋집니다.
    이런 행복하고 평온한 기분을 이어갈 수 있는 OTT 컨텐츠를 추천해드리고 싶습니다. 넷플릭스의 "나의 옆자리 이드님"이라는 애니메이션을 추천드립니다. 
    이 작품은 따뜻한 감성과 아름다운 영상미로 가득한 작품으로, 오늘의 행복한 감정을 더욱 깊이 느낄 수 있게 해줄 거예요. 
    강아지와의 교감, 일상의 소소한 행복을 다루고 있어 오늘 하루의 감정과도 잘 어울릴 것 같습니다.
    행복한 하루 보내셨길 바라며, 내일도 오늘처럼 즐겁고 의미 있는 하루가 되길 응원하겠습니다!
    추천 콘텐츠 : {플랫폼} {콘텐츠}

    예시 3:

    Sending input text: Emoticons Details: {'weather': '흐림', 'emotion': ['행복'], 'activity': ['축구'], 'daily': ['독서']}, 
    Diary: '발목을 삐끗해서 너무 아팠어'}

    날씨는 흐렸지만, 축구를 하며 활기찬 시간을 보내셨군요. 운동은 우리에게 즐거움과 활력을 주는 좋은 활동이에요. 하지만 발목을 삐끗하셔서 많이 아프셨다니 정말 안타깝습니다. 
    그럼에도 불구하고 행복한 감정을 느끼셨다니, 긍정적인 마음가짐이 대단하십니다.
    또한 독서로 마음의 양식도 채우셨네요. 아픈 와중에도 독서를 하신 것을 보니 정신적으로 풍요로운 시간을 보내셨을 것 같습니다.
    이런 상황에서 위로가 되고 힘이 될 수 있는 OTT 컨텐츠를 추천해드리고 싶습니다. 넷플릭스의 "나의 해방일지"라는 드라마를 추천드립니다. 이 작품은 일상의 소소한 행복과 삶의 의미를 찾아가는 과정을 따뜻하게 그려낸 드라마입니다.
    주인공들이 각자의 어려움을 극복해나가는 모습을 보면서 위로와 용기를 얻을 수 있을 거예요. 
    또한 잔잔한 일상의 행복을 그려내어 오늘의 감정과도 잘 어울릴 것 같습니다.
    발목 통증이 빨리 나아지길 바랍니다. 휴식을 취하면서 몸을 잘 돌보세요. 내일은 더 좋은 일만 가득하길 바라겠습니다!
    추천 콘텐츠 : {플랫폼} {콘텐츠}
    """

    # 모델 입력 메시지 (시스템 메시지 + 사용자 메시지 구성)
    print(f"Sending input text: {input_text}")
    messages = [
        SystemMessage(content=system_prompt),  # 시스템 메시지 추가
        HumanMessage(content=input_text),  # 사용자 메시지
    ]

    # Bedrock 모델 호출
    response = llm.invoke(messages)
    return response.content  # Claude 모델 응답 반환


