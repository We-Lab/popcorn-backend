from rest_framework import serializers

from movie.models import Movie, BoxOfficeMovie
from movie.serializers.movie import MovieIdTitleSerializer


class BoxOfficeListSerializer(serializers.ModelSerializer):
    movie = MovieIdTitleSerializer(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'release_date',
            'ticketing_rate',
        )


class BoxOfficeMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            'title_kor',
            'img_url',
            'star_average',
        )


class BoxOfficeDetailSerializer(serializers.ModelSerializer):
    movie = BoxOfficeMovieSerializer(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'release_date',
            'ticketing_rate',
        )

