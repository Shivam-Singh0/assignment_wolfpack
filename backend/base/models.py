from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from PIL import ImageOps, Image
from io import BytesIO
from django.core.files import File

# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Pic(models.Model):
    name = models.TextField(max_length=200, unique=True)
    image = models.ImageField(blank=True, null=True)
    thumb = models.ImageField(blank=True, null=True)
    large = models.ImageField(blank=True, null=True)
    medium = models.ImageField(blank=True, null=True)
    greyscale = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.thumb = self.resizer(self.image, (200, 300))
        self.large = self.resizer(self.image, (1024, 768))
        self.medium = self.resizer(self.image, (500, 500))
        img = Image.open(self.image)
        gray = ImageOps.grayscale(img)
        thumb_io = BytesIO()
        gray.save(thumb_io, 'JPEG', quality=85)
        self.greyscale = File(thumb_io, name=self.name)

        super(Pic, self).save(*args, **kwargs)

    def resizer(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img = img.resize(size, Image.LANCZOS)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
