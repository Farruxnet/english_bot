from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from data.models import Words
from django.utils import timezone
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have an phone_number')

        user = self.model(
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    CHOICES = (
        ('oz', 'O\'zbek'),
        ('uz', 'Узбек'),
        ('ru', 'Руский'),
        ('en', 'Ingliz'),
    )
    tg_id = models.BigIntegerField(default=0)
    phone_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)

    STATUS_CHOICES = (
        ('customer', '1'),
        ('driver', '2'),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=10, null=True, blank=True)
    amount = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    create_at = models.DateTimeField(default = timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name="Foydalanuvchi"
        verbose_name_plural="Foydalanuvchilar"

    @property
    def is_staff(self):
        return self.is_admin

class DayWord(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    words = models.ManyToManyField(Words, null = True, verbose_name = 'Kunlik so\'zlar')
    words_text = models.TextField()
    create_at = models.DateTimeField(default = timezone.now, null = True)

class Ball(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    words = models.ForeignKey(DayWord, on_delete = models.CASCADE, null = True)
    ball = models.IntegerField(default = 0)
    create_at = models.DateTimeField(default = timezone.now, null = True)


class UserNewWord(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    words = models.ManyToManyField(Words, null = True, verbose_name = 'Yodlangan so`zlar')

    create_at = models.DateTimeField(default = timezone.now, null = True)

    def __str__(self):
        return 'so`zlar'




class UserResult(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    word_count = models.IntegerField(default = 0)
    true_answer = models.IntegerField(default = 0)
    false_answer = models.IntegerField(default = 0)

    create_at = models.DateTimeField(default = timezone.now, null = True)

    def __str__(self):
        return self.user












########################
