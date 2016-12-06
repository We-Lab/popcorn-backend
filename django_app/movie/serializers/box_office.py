from rest_framework import serializers

from movie.models import BoxOfficeMovie


class BoxOfficeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'movie_title',
            'release_date',
            'ticketing_rate',
        )
