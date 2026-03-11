# Django REST Framework의 serializer 모듈 import
# → API에서 데이터를 변환(직렬화/역직렬화)할 때 사용
from rest_framework import serializers

# 현재 앱의 CollectedReview 모델 import
# → DB 테이블(stg_movie_reviews)에 매핑된 모델
from .models import CollectedReview


# ============================================================
# CollectedReview 데이터를 API용으로 변환하는 Serializer
# ============================================================
class CollectedReviewSerializer(serializers.ModelSerializer):

    # ------------------------------------------------------------
    # Serializer 설정 클래스
    # ------------------------------------------------------------
    class Meta:

        # 어떤 Django 모델을 기반으로 Serializer를 만들지 지정
        model = CollectedReview

        # API에서 사용할 필드 목록 지정
        # → 모델의 필드 중 아래 항목만 JSON으로 변환됨
        fields = [
            "id",  # DB 기본 키 (Primary Key)
            "title",  # 리뷰 제목
            "review",  # 리뷰 본문
            # "doc_id",       # 중복 방지용 문서 ID
            # "collected_at"  # 데이터 수집 시각
        ]
