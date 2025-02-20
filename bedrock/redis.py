import redis
from datetime import datetime

# Redis 클라이언트 설정
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def save_chat_to_redis(user_id, user_message, bot_response):
    """
    Redis에 챗봇 대화 내용을 저장합니다.

    :param user_id: 사용자 ID
    :param user_message: 사용자가 보낸 메시지
    :param bot_response: 챗봇의 응답
    """
    # 현재 시간 가져오기
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Redis에 저장할 키 생성
    chat_key = f"chat:{user_id}:{timestamp}"

    # 대화 내용 저장
    redis_client.hmset(chat_key, {
        'user_message': user_message,
        'bot_response': bot_response,
        'timestamp': timestamp
    })

    print(f"Saved chat to Redis: {chat_key}")


def get_chat_history_from_redis(user_id):
    """
    Redis에서 특정 사용자의 대화 기록을 가져옵니다.

    :param user_id: 사용자 ID
    :return: 대화 기록 리스트
    """
    # Redis에서 해당 사용자의 모든 대화 키 가져오기
    chat_keys = redis_client.keys(f"chat:{user_id}:*")

    # 대화 기록 리스트 생성
    chat_history = []

    for key in sorted(chat_keys):
        chat_data = redis_client.hgetall(key)
        chat_history.append({
            'timestamp': chat_data.get('timestamp'),
            'user_message': chat_data.get('user_message'),
            'bot_response': chat_data.get('bot_response')
        })

    return chat_history