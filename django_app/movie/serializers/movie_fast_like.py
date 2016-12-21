from rest_framework import serializers

from movie.models import Movie


class MovieFastLikeSerializer(serializers.ModelSerializer):
    """
    빠른 영화평가 직렬화
    """
    class Meta:
        model = Movie
        fields = (
            'id',
            'title_kor',
            'img_url',
            'created_year',
        )

    # 영화 좋아요 작성여부, 댓글 작성여부 추가
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = False
        ret['is_comment'] = False
        request = self.context.get('request')
        if request is not None:
            if request.user.is_authenticated:
                if instance.like_users.filter(id=request.user.pk).exists():
                    ret['is_like'] = True
                if instance.comment_users.filter(id=request.user.pk).exists():
                    ret['is_comment'] = True
        return ret
