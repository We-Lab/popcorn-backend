from rest_framework import serializers

from movie.models import Comment, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    # like_users 필드로 사용자의 좋아요 선택여부 판단 가능
    class Meta:
        model = Comment
        fields = (
            'id',
            'movie',
            'movie_title',
            'author',
            'star',
            'content',
            'likes_count',
            'like_users',
            'created_date',
        )
        read_only_fields = ('movie',)


class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('user', )
