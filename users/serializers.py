from rest_framework import serializers
from .models import User  # MongoEngine 모델과 연결
from mongoengine.errors import NotUniqueError


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)  # 비밀번호 필드 추가
    password_confirmation = serializers.CharField(write_only=True, min_length=6)  # 비밀번호 확인 필드 추가
    nickname = serializers.CharField(max_length=50, required=True)

    def validate(self, data):
        """
        비밀번호와 비밀번호 확인을 검증하는 로직
        """
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        # 비밀번호와 비밀번호 확인이 일치하는지 검증
        if password != password_confirmation:
            raise serializers.ValidationError({
                "password_confirmation": "Passwords do not match"
            })

        return data

    def create(self, validated_data):
        """
        유효성 검사가 완료된 데이터를 사용하여 사용자 저장
        """
        try:
            # 검증된 데이터에서 password_confirmation 키 제거
            validated_data.pop('password_confirmation')

            user = User(
                email=validated_data['email'],
                nickname=validated_data['nickname']
            )
            # 비밀번호 설정 (해싱)
            user.set_password(validated_data['password'])
            user.save()
            return user
        except NotUniqueError:  # 이메일 중복 처리
            raise serializers.ValidationError({
                "email": "This email is already in use"
            })


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        이메일과 비밀번호를 검증
        """
        email = data.get("email")
        password = data.get("password")
        try:
            # 데이터베이스에서 사용자 검색
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")

        # 비밀번호 검증
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        # 인증 성공 시, 사용자 데이터를 반환
        return {"user_id": user.id, "email": user.email}
