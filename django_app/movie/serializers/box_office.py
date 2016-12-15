from rest_framework import serializers

from movie.models import BoxOfficeMovie
from movie.serializers.movie import BoxOfficeDetailSerializer


class BoxOfficeSerializer(serializers.ModelSerializer):
    movie = BoxOfficeDetailSerializer(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'movie_title',
            'release_date',
            'ticketing_rate',
        )
