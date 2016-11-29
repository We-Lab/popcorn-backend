from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator, RegexValidator

from movie.models import Genre, ViewRating, MakingCountry


class MyUserManager(UserManager):
    pass


GENDER_CHOICES = (
    ('M', 'Man'),
    ('W', 'Woman')
)


class MyUser(AbstractUser):
    # 필수 기입정보
    username = models.CharField(max_length=9, unique=True, validators=[RegexValidator(regex='^([a-zA-Z0-9]){4,10}$')])
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13, validators=[MinLengthValidator(10)])
    # 선택 기입정보
    profile_img = models.ImageField(upload_to='user-profile', blank=True)
    favorite_genre = models.ManyToManyField(Genre, blank=True)
    favorite_view_ratting = models.ManyToManyField(ViewRating, blank=True)
    favorite_making_country = models.ManyToManyField(MakingCountry, blank=True)
    # 자동 기입정보
    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ('email', 'gender', 'date_of_birth', 'phone_number')

    def __str__(self):
        return self.get_full_name()

    # phone_number '-' 삭제
    def save(self, *args, **kwargs):
        if '-' in self.phone_number:
            self.phone_number = self.phone_number.replace('-', '')
        super().save(*args, **kwargs)
