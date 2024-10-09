from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model that allows using email as the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password=None):
        """Creates and saves a User"""
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, password=None):
        """Creates and saves a Superuser"""
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']  # Username is required in addition to email

    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
        "Check if user has a specific permission"
        # TODO: Implement permissions if required
        return True
    

    def has_module_perms(self, app_label):
        "Check if user has permissions to view an app"
        # TODO: implement if required
        return True


    @property
    def is_staff(self):
        "Check if user is a staff"
        # TODO: implement if required
        return self.is_staff
