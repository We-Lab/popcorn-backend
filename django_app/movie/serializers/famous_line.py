from rest_framework import serializers

from movie.models import FamousLine, FamousLike


class FamousLineSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    # movie = serializers.StringRelatedField()

    class Meta:
        model = FamousLine
        fields = (
            'id',
            'movie',
            'movie_title',
            'actor',
            'actor_kor_name',
            'actor_character_name',
            'actor_img_url',
            'author',
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


class FamousLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FamousLike
        fields = ('user', )
