from rest_framework import generics
from rest_framework import permissions

from movie.models import Movie
from movie.serializers.movie_fast_like import MovieFastLikeSerializer
from mysite.utils.custom_pagination import LargeResultsSetPagination


class MovieFastLike(generics.ListAPIView):
    """
    유저가 별점을 달지 않은 영화만 20개씩 출력합니다

    """
    serializer_class = MovieFastLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Movie.objects.exclude(comment__author=self.request.user.pk).exclude(img_url='').order_by('-create')

