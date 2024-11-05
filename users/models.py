from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, username, role, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, role, password=None):
        user = self.create_user(
            email=email,
            username=username,
            role=role,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('lawyer', 'Lawyer'),
        ('admin', 'Admin'),
        ('client', 'Client'),
    ]
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Foreign key to associate clients with their lawyers
    lawyer = models.ForeignKey('self', null=True, blank=True, related_name='lawyer_clients', on_delete=models.SET_NULL)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class LoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time}"

class Client(models.Model):
    lawyer = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)  # Each client is linked to one lawyer
    name = models.CharField(max_length=100)
    # Add any additional fields for the client as needed

    def __str__(self):
        return self.name
