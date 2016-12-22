""" 빠른 별점달기 view module
1. 유저가 별점을 빠르게 추가하는 단축 페이지입니다.
2. ios 전용입니다.
"""
from rest_framework import generics
from rest_framework import permissions

from movie.models import Movie
from movie.serializers.movie_fast_like import MovieFastLikeSerializer
from mysite.utils.custom_pagination import LargeResultsSetPagination


class MovieFastLike(generics.ListAPIView):
    """
    1. 유저가 별점을 달지 않은 영화만 출력
    2. 20개씩 pagination
    """
    serializer_class = MovieFastLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Movie.objects.exclude(comment__author=self.request.user.pk).exclude(img_url='').order_by('-create')

