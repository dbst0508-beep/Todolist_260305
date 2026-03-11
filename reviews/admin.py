from django.contrib import admin

from .models import CollectedReview


@admin.register(CollectedReview)


# CollectedReview 모델의 관리자 페이지 설정 클래스
class CollectedReviewAdmin(admin.ModelAdmin):

    # ------------------------------------------------------------
    # 관리자 목록 화면에서 표시할 컬럼 설정
    # ------------------------------------------------------------
    # id           : 데이터 기본 키
    # title        : 리뷰 제목
    # doc_id       : 중복 방지용 문서 ID
    # collected_at : 데이터 수집 시각
    list_display = ("id", "title")

    # ------------------------------------------------------------
    # 관리자 페이지 검색 기능 설정
    # ------------------------------------------------------------
    # title  : 제목 기준 검색
    # review : 본문 기준 검색
    # 관리자 검색창에서 키워드를 입력하면
    # 해당 필드를 기준으로 DB 검색 수행
    search_fields = ("title", "review")
