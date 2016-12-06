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
            'author',
            'content',
            'likes_count',
            'like_users',
            'created_date',
        )
        read_only_fields = ('movie',)


class FamousLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FamousLike
        fields = ('user', )
