from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import User

class RegisterView(APIView):
    """
    회원가입 API
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # DB 저장
            return Response(
                {"success": True, "message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
class LoginView(APIView):
    """
       로그인 API (JWT 발급 추가)
       """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # JWT 발급
            user_id = serializer.validated_data["user_id"]
            refresh = RefreshToken.for_user(User.objects.get(id=user_id))  # User 객체 전달
            return Response(
                {
                    "success": True,
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

