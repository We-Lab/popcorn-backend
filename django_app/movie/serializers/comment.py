from rest_framework import serializers

from member.serializers import UserSerializer
from movie.models import Comment
from movie.serializers.movie import MovieSerializer


class CommentSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'movie',
            'author',
            'content',
            'created_date',
        )
