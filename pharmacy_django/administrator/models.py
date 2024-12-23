from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager):
    '''
        Manager for base user
    '''
    
    def create_user(self, username: str, age: int, gender: str, primary_phone_number: str,  role: str, is_verified: bool, first_name: str, last_name: str, email: models.EmailField = '', password: str = '', secondary_phone_number: str = '', is_staff: bool = False, is_active: bool = True, is_superuser: bool = False):
        '''
            Create user method for the manager
        '''
        
        if not username:
            raise ValueError("Username of the user must be provided.")
        if not age:
            raise ValueError("Age of the user must be provided.")
        if not gender:
            raise ValueError("Gender of the user must be provided.")
        if not primary_phone_number:
            raise ValueError("Primary Phone Number of the user must be provided.")
        if not role:
            raise ValueError("Role of the user must be provided.")
        if not first_name:
            raise ValueError("First name of the user must be provided.")
        if not last_name:
            raise ValueError("Last name of the user must be provided.")
        
        # As is_verified is a boolean, using the conventional method will fire if is_verified is set to False, leading to errors
        try:
            is_verified
        except NameError:
            raise ValueError("It must be provided if the user is verified or not.")
        
        if gender not in ['Male', 'Female', 'Other']:
            raise ValueError('The valid values for gender can only be \'Male\', \'Female\' or \'Other\'')
        
        if role not in ['Admin', 'Doctor', 'Employee', 'Patient']:
            raise ValueError('The valid values for role can only be \'Admin\', \'Doctor\', \'Employee\' or \'Patient\'')
        
        user = self.model(
            username = username,
            age = age,
            gender = gender,
            primary_phone_number = primary_phone_number,
            role = role,
            is_verified = is_verified,
            email = email,
            first_name = first_name,
            last_name = last_name
        )
        user.secondary_phone_number = secondary_phone_number
        user.is_staff = is_staff
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, username: str, age: int, gender: str, primary_phone_number: str,  role: str, first_name: str, last_name: str, email: models.EmailField = '', password: str = '', secondary_phone_number: str = ''):
        user = self.create_user(
            username=username,
            age=age,
            gender=gender,
            primary_phone_number=primary_phone_number,
            role=role,
            is_verified=True,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            secondary_phone_number=secondary_phone_number,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.save()
        
        return user
    
    
class User(AbstractUser):
    
    '''
        Stores the details of the base user model used for authentication. Serves as a template for Patient, Doctor and Employees.
        
        Implicit fields created from AbstractUser: username, password, email, first_name, last_name, is_active, is_staff,
            is_superuser, last_login and date_joined
    '''
    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.EmailField(max_length=150, blank=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)], blank=False)
    
    genderChoices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    gender = models.CharField(choices=genderChoices, max_length=6, blank=False)
    
    primary_phone_number = models.CharField(max_length=15, blank=False)
    secondary_phone_number = models.CharField(max_length=15, blank=True)
    
    roleChoices = (
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Pharmacy', 'Pharmacy'),
        ('FrontDesk', 'FrontDesk'),
        ('Patient', 'Patient')
    )
    role = models.CharField(choices=roleChoices, max_length=9, blank=False)
    
    is_verified = models.BooleanField(default=False, blank=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
        
    def __str__(self):
        return f"Name: {self.username}"
