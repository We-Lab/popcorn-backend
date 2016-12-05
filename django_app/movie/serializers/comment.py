from rest_framework import serializers

from member.models import MyUser
from member.serializers import UserSerializer
from movie.models import Comment, Movie, CommentLike
from movie.serializers.movie import MovieSerializer


class MovieTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title_kor', )


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', )


class CommentSerializer(serializers.ModelSerializer):
    movie = MovieTitleSerializer(read_only=True)
    author = UsernameSerializer(read_only=True)
    # like_users = UsernameSerializer(read_only=True, many=True)

    # like_users 필드로 사용자의 좋아요 선택여부 판단 가능
    class Meta:
        model = Comment
        fields = (
            'id',
            'movie',
            'author',
            'star',
            'content',
            'likes_count',
            'like_users',
            'created_date',
        )


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('user', )
