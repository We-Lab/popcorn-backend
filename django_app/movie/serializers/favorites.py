from rest_framework import serializers

from member.models import MyUser


class UserFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'favorite_genre',
            'favorite_grade',
            'favorite_making_country',
        )
