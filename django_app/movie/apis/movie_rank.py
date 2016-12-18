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
