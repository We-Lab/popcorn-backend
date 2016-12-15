from rest_framework import serializers

from movie.models import BoxOfficeMovie
from movie.serializers.movie import BoxOfficeDetailSerializer, BoxOfficeDetailSerializerIOS


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


class BoxOfficeSerializerIOS(serializers.ModelSerializer):
    movie = BoxOfficeDetailSerializerIOS(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'movie_title',
            'release_date',
            'ticketing_rate',
        )
