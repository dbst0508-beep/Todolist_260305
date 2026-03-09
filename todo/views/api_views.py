# from rest_framework import APIView
# from rest_framework.response import Response
# from rest_framework import status

from rest_framework import viewsets
from ..models import Todo
from interaction.models import TodoLike, TodoBookmark, TodoComment
from rest_framework.response import Response

# 인증된 사용자만 접근 가능하도록 하는 권한 클래스
from rest_framework.permissions import IsAuthenticated
from ..serializers import TodoSerializer  # 시리얼라이즈 불러오기
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class TodoListPagination(PageNumberPagination):

    page_size = 3
    # 한 페이지에 기본적으로 보여줄 데이터 개수

    page_size_query_param = "page_size"
    # URL 쿼리 파라미터로 페이지 크기 변경 가능
    # 예: /todo/viewsets/view/?page_size=5

    max_page_size = 50
    # 사용자가 설정할 수 있는 최대 페이지 크기 제한
    # 예: page_size=100 요청 시 최대 50까지만 허용


class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer
    permission_classes = [AllowAny]  # ← 10번에서 변경됨

    def list(self, request, *args, **kwargs):

        # queryset 필터링
        qs = self.filter_queryset(self.get_queryset())

        # pagination 처리
        page = self.paginate_queryset(qs)

        if page is not None:

            # serializer 실행
            serializer = self.get_serializer(
                page,
                many=True,
                context={"request": request},
            )

            return Response(
                {
                    "data": serializer.data,
                    # 현재 페이지
                    "current_page": int(request.query_params.get("page", 1)),
                    # 전체 페이지 수
                    "page_count": self.paginator.page.paginator.num_pages,
                    # 다음 페이지 존재 여부
                    "next": self.paginator.get_next_link() is not None,
                    # 이전 페이지 존재 여부
                    "previous": self.paginator.get_previous_link() is not None,
                }
            )
        # pagination이 없는 경우
        # ---------------------------------------------
        serializer = self.get_serializer(
            qs,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "data": serializer.data,
                "current_page": 1,
                "page_count": 1,
                "next": False,
                "previous": False,
            }
        )
        # 좋아요 토글 API

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):

        # 현재 Todo 가져오기
        todo = self.get_object()

        # 로그인한 사용자
        user = request.user

        # 좋아요 존재 확인
        obj, created = TodoLike.objects.get_or_create(todo=todo, user=user)

        # 새로 생성된 경우 → 좋아요 ON
        if created:
            liked = True

        # 이미 존재 → 삭제 → 좋아요 OFF
        else:
            obj.delete()
            liked = False

        # 전체 좋아요 개수 계산
        like_count = TodoLike.objects.filter(todo=todo).count()

        # 응답
        return Response({"liked": liked, "like_count": like_count})

    # 북마크 토글 API
    # 좋아요와 동일한 구조
    # -----------------------------------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):

        # 현재 Todo
        todo = self.get_object()

        # 로그인 사용자
        user = request.user

        # 북마크 생성 또는 조회
        obj, created = TodoBookmark.objects.get_or_create(todo=todo, user=user)

        # 북마크 ON
        if created:
            bookmarked = True

        # 북마크 OFF
        else:
            obj.delete()
            bookmarked = False

        # 전체 북마크 수
        bookmark_count = TodoBookmark.objects.filter(todo=todo).count()

        return Response({"bookmarked": bookmarked, "bookmark_count": bookmark_count})

    # 댓글 등록 API
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):

        # Todo 가져오기
        todo = self.get_object()

        # 로그인 사용자
        user = request.user

        # 댓글 내용 가져오기
        content = (request.data.get("content") or "").strip()

        # 댓글 내용 검증
        if not content:
            return Response({"detail": "content is required"}, status=400)

        # 댓글 생성
        TodoComment.objects.create(todo=todo, user=user, content=content)

        # 댓글 개수 계산
        comment_count = TodoComment.objects.filter(todo=todo).count()

        return Response({"comment_count": comment_count})
