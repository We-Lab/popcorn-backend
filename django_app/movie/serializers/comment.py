from rest_framework import serializers

from member.serializers import MyInfoSerializer
from movie.models import Comment, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    """
    댓글 직렬화
    배우정보 nested
    """
    author = MyInfoSerializer(read_only=True)

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

    # 유저의 좋아요 작성여부 추가
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
    """
    댓글 좋아요 직렬화
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('user', )


class MyCommentStarSerializer(serializers.ModelSerializer):
    """
    나의 별점 직렬화
    """
    class Meta:
        model = Comment
        fields = ('star', )
