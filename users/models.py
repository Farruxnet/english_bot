from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from data.models import Words

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
    tg_id = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)

    STATUS_CHOICES = (
        ('customer', 'Mijoz'),
        ('driver', 'Haydovchi'),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=10, null=True, blank=True)
    amount = models.IntegerField(default=0)
    step = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
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


class UserNewWord(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    new = models.ManyToManyField(Words, verbose_name = 'Yangi so`zlar', related_name = 'newword')
    saved = models.ManyToManyField(Words, verbose_name = 'Yot olingan so`zlar', related_name = 'savedword')
    
    def __str__(self):
        return 'so`zlar'


















########################
