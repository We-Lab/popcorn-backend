from rest_framework import serializers

from movie.models import FamousLine, Actor, Movie
from movie.serializers.comment import UsernameSerializer, MovieTitleSerializer


class FamousLineSerializer(serializers.ModelSerializer):
    movie = MovieTitleSerializer(read_only=True)
    author = UsernameSerializer(read_only=True)

    class Meta:
        model = FamousLine
        fields = (
            'movie',
            'actor',
            'author',
            'content',
            'created_date',
        )

