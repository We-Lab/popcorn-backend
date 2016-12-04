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

    class Meta:
        model = Comment
        fields = (
            'id',
            'movie',
            'author',
            'star',
            'content',
            'created_date',
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'movie',
            'author',
            'star',
            'content',
            'created_date',
        )


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('user', )
