from rest_framework import serializers

from member.serializers import UserSerializer
from movie.models import Comment


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
