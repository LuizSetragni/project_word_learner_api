from venv import logger
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

class Word(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    phrase_1 = models.TextField(blank=True, null=True)
    phrase_2 = models.TextField(blank=True, null=True)
    phrase_3 = models.TextField(blank=True, null=True)
    synonym_1 = models.CharField(max_length=100, blank=True, null=True)
    synonym_2 = models.CharField(max_length=100, blank=True, null=True)
    synonym_3 = models.CharField(max_length=100, blank=True, null=True)
    meaning_1 = models.TextField(blank=True, null=True)
    meaning_2 = models.TextField(blank=True, null=True)
    meaning_3 = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self):
        return self.content

class UserManager(BaseUserManager):
    def create_user(self, email, name, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        logger.info("Novo usuário criado - Email: %s, Nome: %s, Username: %s", email, name, username)
        
        return user

    def create_superuser(self, email, name, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, username, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username
