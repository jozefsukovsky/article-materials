from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.sessions.models import AbstractBaseSession, BaseSessionManager
from django.db import models
from django.utils import timezone


class SessionManager(BaseSessionManager):
    use_in_migrations = True


class PublicSession(AbstractBaseSession):

    class Meta(AbstractBaseSession.Meta):

        db_table = "django_session_public"
    
    objects = SessionManager()

    @classmethod
    def get_session_store_class(cls):
        from .session import SessionStore
        return SessionStore


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a new user with the given email and password."""
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User instance with the given email and password."""
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField('Email Address', unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date_activated = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.email
