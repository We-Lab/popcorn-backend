from rest_framework import serializers

from member.models import MyUser


class UserFavoritesSerializer(serializers.ModelSerializer):
    """
    유저 취향정보 직렬화
    """
    class Meta:
        model = MyUser
        fields = (
            'favorite_genre',
            'favorite_grade',
            'favorite_making_country',
        )
