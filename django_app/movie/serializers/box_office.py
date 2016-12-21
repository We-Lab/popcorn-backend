from rest_framework import serializers

from movie.models import BoxOfficeMovie
from movie.serializers.movie import BoxOfficeDetailSerializer, BoxOfficeDetailSerializerIOS


class BoxOfficeSerializer(serializers.ModelSerializer):
    """
    박스오피스 직렬화
    영화정보 nested
    """
    movie = BoxOfficeDetailSerializer(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'movie_title',
            'release_date',
            'ticketing_rate',
        )


class BoxOfficeSerializerIOS(serializers.ModelSerializer):
    """
    박스오피스 직렬화 ios전용
    영화정보 nested
    """
    movie = BoxOfficeDetailSerializerIOS(read_only=True)

    class Meta:
        model = BoxOfficeMovie
        fields = (
            'rank',
            'movie',
            'movie_title',
            'release_date',
            'ticketing_rate',
        )

    # 좋아요 여부, 댓글작성 여부 추가
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
