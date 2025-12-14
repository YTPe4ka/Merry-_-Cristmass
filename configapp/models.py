from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username kiritilishi shart!')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser is_admin=True bo‘lishi kerak!')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True bo‘lishi kerak!')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username
    @property
    def is_superuser(self):
        return self.is_admin

class Todo(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='todos')
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True, null=True)
    completed=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    



# ///////////////////////////////////// about me :>

from django.db import models

class Home(models.Model):
    name = models.CharField(max_length=150)
    roles = models.CharField(max_length=255, blank=True)  # comma separated
    background = models.ImageField(upload_to='hero/', blank=True, null=True)

    def __str__(self):
        return self.name

class About(models.Model):
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    birthday = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    profile_image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return "About"

class ResumeEntry(models.Model):
    section = models.CharField(max_length=50)  # 'education' or 'experience'
    title = models.CharField(max_length=200)
    date_from = models.CharField(max_length=50, blank=True)
    date_to = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text='Ordering for resume items; lower appear first')

    def __str__(self):
        return f"{self.section} - {self.title}"

    class Meta:
        ordering = ['order', '-id']

class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    details_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=50, help_text='Skill level as percent 0-100')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.level}%)"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ContactInfo(models.Model):
    """Single-row editable contact information for footer/contact section."""
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return "Site contact info"

    class Meta:
        verbose_name = 'Contact Info'
        verbose_name_plural = 'Contact Info'
