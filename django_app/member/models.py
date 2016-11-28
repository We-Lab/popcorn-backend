from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from movie.models import Genre, ViewRating, MakingCountry


class MyUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            last_name,
            first_name,
            phone_number,
            password=None,
            ):
        user = self.model(
            email=email,
            last_name=last_name,
            first_name=first_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            password=None,
            ):
        user = self.model(
            email=email,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    # 필수 기입정보
    email = models.EmailField(max_length=50, unique=True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13)
    # 선택 기입정보
    profile_img = models.ImageField(upload_to='user-profile', blank=True)
    favorite_genre = models.ManyToManyField(Genre, blank=True)
    favorite_view_ratting = models.ManyToManyField(ViewRating, blank=True)
    favorite_making_country = models.ManyToManyField(MakingCountry, blank=True)
    # 자동 기입정보
    date_joined = models.DateTimeField(auto_now_add=True)
    # 권한 정보
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'phone_number', 'date_of_birth']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s%s' % (self.last_name, self.first_name)

    def get_short_name(self):
        return self.first_name

    # phone_number '-' 삭제
    def save(self, *args, **kwargs):
        if '-' in self.phone_number:
            self.phone_number = self.phone_number.replace('-', '')
        super().save(*args, **kwargs)


