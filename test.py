import os
from dotenv import load_dotenv
from urllib.parse import quote

# .env 파일 로드
load_dotenv()

# 환경 변수 읽기
db_name = os.getenv('MONGO_DB_NAME', 'momo')
hosts = os.getenv('MONGO_DB_HOST', 'localhost')  # 쉼표로 구분된 호스트 목록
port = os.getenv('MONGO_DB_PORT', '27017')
username = os.getenv('MONGO_DB_USERNAME', 'admin')
password = os.getenv('MONGO_DB_PASSWORD', 'k8spass#')  # URL 인코딩을 위해 변경할 필요 있음
replica_set = os.getenv('MONGO_DB_REPLICA_SET_PART', 'rs0')

# 비밀번호 URL 인코딩 (특수문자 처리)
encoded_password = quote(password)

# 호스트가 여러 개일 경우, 각 호스트와 포트를 함께 조합
host_part = ",".join([f"{host}:{port}" for host in hosts.split(",")])

# 인증 정보 설정
auth_part = f"{username}:{encoded_password}@" if username and encoded_password else ""

# replicaSet 옵션 추가
replica_set_part = f"&replicaSet={replica_set}" if replica_set else ""

# 최종 MongoDB URI 생성
MONGO_URI = f"mongodb://{auth_part}{host_part}/{db_name}?authSource=admin{replica_set_part}"

# MongoDB 연결
print(MONGO_URI)


# mongodb://admin:k8spass#@192.168.56.109:27017,192.168.56.110:27017,192.168.56.111:27017/momo?authSource=admin&replicaSet=rs0
# mongodb://admin:k8spass%23@192.168.56.109:27017,192.168.56.110:27017,192.168.56.111:27017/momo?authSource=admin&replicaSet=rs0

