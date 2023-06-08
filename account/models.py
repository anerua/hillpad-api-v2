from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from helpers.models import TrackingModel


class CustomUserManager(UserManager):
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not "first_name" in extra_fields or not extra_fields["first_name"]:
            raise ValueError("The given first name must be set")
        if not "last_name" in extra_fields or not extra_fields["last_name"]:
            raise ValueError("The given last name must be set")
        if not "role" in extra_fields or not extra_fields["role"]:
            raise ValueError("The role of the user must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_staff(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("role") != User.ADMIN:
            raise ValueError("Superuser must have role=Admin.", f"You used {extra_fields.get('role')}")
        
        return self._create_user(email, password, **extra_fields) 


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):

    CLIENT = "CLIENT"
    SPECIALIST = "SPECIALIST",
    SUPERVISOR = "SUPERVISOR"
    ADMIN = "ADMIN"
    USER_ROLE_CHOICES = (
        (CLIENT, _("Client role")),
        (SPECIALIST, _("Data Entry Specialist role")),
        (SUPERVISOR, _("Data Entry Supervisor role")),
        (ADMIN, _("Admin role")),
    )

    MALE = "MALE"
    FEMALE = "FEMALE"
    GENDER_CHOICES = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    )
    
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(_("role"), max_length=6, choices=USER_ROLE_CHOICES)
    
    gender = models.CharField(_("gender"), max_length=6, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateTimeField(_("date of birth"), blank=True, null=True)
    nationality = models.CharField(_("nationality"), max_length=32, blank=True)
    country_of_residence = models.CharField(_("country of residence"), max_length=32, blank=True)

    is_staff = models.BooleanField(
        _("Is a staff?"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Is active?"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    email_verified = models.BooleanField(
        _("Email is verified?"),
        default=False,
        help_text=_(
            "Designates whether this user's email is verified."
        ),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]
