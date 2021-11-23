from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from mapbox_location_field.models import LocationField
from ckeditor.fields import RichTextField

class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': username})

    def has_module_perms(self, app_label):
        return True 
    
    def has_perm(self, perm, ob=None):
        return True

class User(AbstractUser):
    DEVICE_TYPE = (
        ('android', 'Android'),
        ('ios', 'IOS'),
    )
    PROVIDER_TYPE = (
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('apple', 'Apple'),
        ('github', 'GitHub'),
        ('demo_app', 'Demo App'),
        ('guest', 'Guest'),
    )
    username = None
    first_name = models.CharField(max_length=255, blank=True)    
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE)
    provider_user_id = models.CharField(max_length=255, blank=True)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPE, default='demo_app')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or 'Guest User'

    class Meta:
        ordering = ["id", "email"]
        db_table = 'users'

    objects = UserManager()


class PushNotification(models.Model):
    title = models.CharField(
        max_length=255, help_text="Add notification title here.")
    message = models.TextField(
        null=True, blank=True, help_text="Add notification message here.")
    image = models.ImageField(
        upload_to='notification-image', null=True, blank=True, help_text="Image view on recived notification.")

    def __str__(self):
        return f"Push Notification {self.title}"

    class Meta:
        verbose_name = "Send Push Notification"
        verbose_name_plural = "Send Push Notifications"
        db_table = 'push_notification'

class MapHistory(models.Model):
    destination_latitude = models.DecimalField(max_digits=50, decimal_places=15)
    destination_longitude = models.DecimalField(max_digits=50, decimal_places=15)
    location = LocationField()
    class Meta:
        verbose_name = "Map History"
        verbose_name_plural = "Map History"
        
class ExcelFilesUpload(models.Model):
    Files = models.FileField(upload_to="upload/Excel")
    
    
class Post(models.Model):
    name = models.CharField(max_length=500)
    description = RichTextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)