from rest_framework import serializers

from movie.models import Movie, BoxOfficeMovie


class BoxOfficeMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            'title_kor',
            'img_url',
        )


class BoxOfficeSerialize(serializers.ModelSerializer):
    movie = BoxOfficeMovieSerializer(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'movie',
            'release_date',
            'ticketing_rate',
        )


