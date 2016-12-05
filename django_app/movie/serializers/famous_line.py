from rest_framework import serializers

from movie.models import FamousLine, FamousLike
from movie.serializers.comment import UsernameSerializer, MovieTitleSerializer


class FamousLineSerializer(serializers.ModelSerializer):
    movie = MovieTitleSerializer(read_only=True)
    author = UsernameSerializer(read_only=True)
    # like_users = UsernameSerializer(read_only=True, many=True)

    class Meta:
        model = FamousLine
        fields = (
            'id',
            'movie',
            'actor',
            'author',
            'content',
            'likes_count',
            'like_users',
            'created_date',
        )


class FamousLikeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)

    class Meta:
        model = FamousLike
        fields = ('user', )
