# 1. 빌드용 컨테이너 (builder stage)
FROM python:3.13.1-alpine AS builder

WORKDIR /app

# 필수 패키지 설치
RUN apk update && apk add --no-cache gcc musl-dev libpq-dev

# 최신 pip 사용
RUN pip install --upgrade pip

# 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 실행용 컨테이너 (최종 이미지)
FROM python:3.13.1-alpine

WORKDIR /app

# 빌드 단계에서 설치한 패키지를 복사
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 소스 코드 복사
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

