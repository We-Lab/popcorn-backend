from rest_framework import serializers

from movie.models import Movie


class RankSerializer(serializers.ModelSerializer):
    star_average = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title_kor',
            'created_year',
            'img_url',
            'star_average',
            'likes_count',
            'like_users',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = False
        request = self.context.get('request')
        if request is not None:
            if request.user.is_authenticated:
                if instance.like_users.filter(id=request.user.pk).exists():
                    ret['is_like'] = True
        return ret
