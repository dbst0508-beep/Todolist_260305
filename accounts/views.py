# jwt사용으로 인해 세션 로그인은 더 이상 필요 없음
from django.contrib.auth import logout

# DRF APIView 사용
from rest_framework.views import APIView

# API 응답 객체
from rest_framework.response import Response

# HTTP 상태 코드
from rest_framework import status

# 모든 사용자 접근 허용
from rest_framework.permissions import AllowAny


# 회원가입 데이터 검증 Serializer
from .serializers import SignupSerializer

# 로그인 한 사람만 접근 가능
from rest_framework.permissions import IsAuthenticated


class SignupAPIView(APIView):

    # 로그인하지 않은 사용자도 접근 가능
    permission_classes = [AllowAny]

    # POST 요청 처리
    def post(self, request):

        # 요청 데이터(request.data)를 Serializer에 전달
        serializer = SignupSerializer(data=request.data)

        # 데이터 검증
        # raise_exception=True → 검증 실패 시 자동으로 에러 응답 반환
        serializer.is_valid(raise_exception=True)

        # 검증 완료 후 사용자 생성
        serializer.save()

        # 회원가입 성공 응답
        return Response({"detail": "회원가입 완료"}, status=status.HTTP_201_CREATED)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        )


# # 세션 로그인 API < jwt 변환하면서 urls.py 에서 토큰으로 처리 됨
# # -----------------------------
# class SessionLoginAPIView(APIView):

#     # 로그인하지 않은 사용자도 접근 가능
#     permission_classes = [AllowAny]

#     # POST 요청 처리
#     def post(self, request):

#         # 요청 데이터에서 username, password 추출
#         username = request.data.get("username", "")
#         password = request.data.get("password", "")

#         # 사용자 인증
#         # username / password가 맞는지 확인
#         user = authenticate(request, username=username, password=password)

#         # 인증 실패
#         if not user:
#             return Response(
#                 {"detail": "아이디/비밀번호가 올바르지 않습니다."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # 인증 성공 → 세션 로그인 처리
#         login(request, user)

#         # 로그인 성공 응답
#         return Response({"detail": "로그인 성공"}, status=status.HTTP_200_OK)


# 세션 로그아웃 API
# -----------------------------
class SessionLogoutAPIView(APIView):

    # POST 요청 처리
    def post(self, request):

        # 현재 로그인된 사용자 세션 종료
        logout(request)

        # 로그아웃 성공 응답
        return Response({"detail": "로그아웃"}, status=status.HTTP_200_OK)
