import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
import jwt
from jwt import PyJWKClient

COGNITO_USER_POOL_ID = "ap-northeast-2_106cO5ApN"
COGNITO_REGION = "ap-northeast-2"
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

class CognitoUser:
    """ Cognito 인증된 사용자 객체 """
    def __init__(self, token_data):
        self.token_data = token_data
        self.username = token_data.get("sub", "")
        self.email = token_data.get("email", "")
        self.is_authenticated = True  # ✅ DRF 인증을 위해 필요

    def __str__(self):
        return f"CognitoUser({self.username})"

class CognitoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None  # 인증 실패 시 None 반환

        token = auth_header.split("Bearer ")[-1]
        if not token:
            raise AuthenticationFailed("Token is missing")

        decoded_token = self.verify_jwt(token)
        if not decoded_token or "sub" not in decoded_token:
            raise AuthenticationFailed("Invalid token: Missing user ID")

        return (CognitoUser(decoded_token), None)  # ✅ CognitoUser 객체 반환

    def verify_jwt(self, token):
        """ PyJWT를 사용하여 Cognito JWT 토큰 검증 """
        jwks_client = PyJWKClient(JWKS_URL)

        # signing_key를 가져올 때는 JWT 토큰 전체를 사용해야 합니다.
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        try:
            # JWT 검증 및 디코딩
            decoded_token = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience="7et4jghd0tr18bmml2ci1mu73o",  # ✅ Cognito App Client ID
                issuer=COGNITO_ISSUER,
            )

            # 디코딩 후 사용자 고유 ID (`sub`)를 출력하거나 활용할 수 있습니다.
            user_sub = decoded_token.get("sub")  # 사용자 고유 ID 가져오기
            print(f"User Sub: {user_sub}")

            return decoded_token

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid token: {str(e)}")
