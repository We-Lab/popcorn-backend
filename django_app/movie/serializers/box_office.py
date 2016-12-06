from rest_framework import serializers

from movie.models import BoxOfficeMovie
from movie.serializers.movie import MovieSerializer


class BoxOfficeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'movie_title',
            'release_date',
            'ticketing_rate',
        )
