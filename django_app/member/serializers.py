from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from member.models import MyUser


class RegistrationSerializer(RegisterSerializer):
    username = serializers.RegexField(regex='^([a-zA-Z0-9]){4,10}$', required=True, help_text='영어/숫자 사용가능 4~10자')
    nickname = serializers.RegexField(regex='^([가-힣a-zA-Z0-9]){4,10}$', required=True, help_text='한글/영어/숫자 사용가능 4~10자')
    gender = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    phone_number = serializers.RegexField(regex='^([0-9]){10,13}$', required=False, help_text='"-" 없이 숫자만 기입가능')
    profile_img = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        return {
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'profile_img': self.validated_data.get('profile_img', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user.nickname = self.cleaned_data['nickname']
        user.gender = self.cleaned_data['gender']
        user.phone_number = self.cleaned_data['phone_number']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.profile_img = self.cleaned_data['profile_img']

        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'nickname',
            'email',
            'gender',
            'date_of_birth',
            'phone_number',
            'profile_img',
            'favorite_genre',
            'favorite_grade',
            'favorite_making_country',
        )
        read_only_fields = ('username', )


class MyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id',
            'nickname',
            'profile_img',
        )
