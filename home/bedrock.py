from langchain.schema import HumanMessage
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
def bedrock_response(input_text):
    # Bedrock 모델 클라이언트 초기화
    llm = ChatBedrock(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name=AWS_REGION,  # AWS 리전 설정
    )

    # 모델 입력 및 호출
    print(f"Sending input text: {input_text}")
    message = HumanMessage(content=input_text)
    response = llm.invoke([message])
    return response.content  # Claude 모델 응답 반환
