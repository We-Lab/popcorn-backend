""" 영화 랭킹 view module
1. 영화 평균별점과 좋아요 개수로 ordering 하는 랭킹 view 입니다.
2. 각 60개씩 상위 리스트를 출력하고 20개씩 pagination 합니다.
"""
from rest_framework import generics

from movie.models import Movie
from movie.serializers.movie_rank import RankSerializer
from mysite.utils.custom_pagination import RankResultsSetPagination


class StarRankView(generics.ListAPIView):
    serializer_class = RankSerializer
    pagination_class = RankResultsSetPagination
    queryset = Movie.objects.order_by('-star_average')[:60]


class LikeRankView(generics.ListAPIView):
    serializer_class = RankSerializer
    pagination_class = RankResultsSetPagination
    queryset = Movie.objects.order_by('-likes_count')[:60]
