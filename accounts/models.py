from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Department(models.Model):
    name = models.CharField(max_length=50)
    department_head = models.CharField(max_length=100)
    amount = models.IntegerField()
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class EmplyeeCode(models.Model):
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.code

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_ITstaff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department', 'is_ITstaff']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
