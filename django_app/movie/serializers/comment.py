from rest_framework import serializers

from member.serializers import MyInfoSerializer
from movie.models import Comment, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    author = MyInfoSerializer(read_only=True)

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
            'created',
        )
        read_only_fields = ('movie',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = False
        request = self.context.get('request')
        if request is not None:
            if request.user.is_authenticated:
                if instance.like_users.filter(id=request.user.pk).exists():
                    ret['is_like'] = True
        return ret


class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('user', )


class MyCommentStarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('star', )
