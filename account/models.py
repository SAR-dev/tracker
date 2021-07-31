from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save

class AccountManager(BaseUserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, email, first_name, last_name, username, password):
        if not email:
            raise ValueError('Email address is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        if not username:
            raise ValueError('Username is required')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(email=self.normalize_email(email),
                                first_name=first_name, last_name=last_name, username=username,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=25, unique=True, validators=[
        RegexValidator(
            regex='^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,25}$',
            message="Invalid Username format! Username should be between 3-50 characters. Use hyphen '-' between letters if needed. ",
        ),
    ])
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        super(Account, self).save(*args, **kwargs)
        
    
    def __str__(self):
        return str(self.username)

    class Meta:
       ordering = ['-id']
