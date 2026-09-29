from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
      ####test
    def create_candiate_user(self, email, name, mobile, password=None, password2=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            mobile = mobile
        )


    # def create_AdminModel_user(self, email_id, password=None):
    #     """
    #     Creates and saves a User with the given email and password.
    #     """
    #     if not email_id:
    #         raise ValueError('Users must have an email address')

    #     user = self.model(
    #         email_id=self.normalize_email(email_id),
    #         password=password
           
    #     )

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password=password, **extra_fields)
    





class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    company_name= models.CharField(max_length=100)
    username= models.CharField(max_length=100)
    short_name= models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    short_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    contact_no = models.CharField(max_length=15)
    footer_message = models.TextField()
    director_name = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=6)
    state = models.CharField(max_length=100)
    state_no_numeric = models.CharField(max_length=3)
    VAT_TIN = models.CharField(max_length=300)
    CST_TIN = models.CharField(max_length=300)
    C_Excise_Range = models.CharField(max_length=300)
    Commissionerate = models.CharField(max_length=300)
    C_Excise_Reg_No = models.CharField(max_length=300)
    PLA_No = models.CharField(max_length=300)
    Service_Tax_No = models.CharField(max_length=300)
    Import_Export_Code = models.CharField(max_length=300)
    ARN_No = models.CharField(max_length=300)
    Export_House_No = models.CharField(max_length=300)
    Udyog_Aadhar_No = models.CharField(max_length=300)
    Vat_Tin_Date = models.DateField(null=True)  # Example of nullable DateField
    Cst_Tin_Date = models.DateField(null=True)  # Example of nullable DateField
    Subject_To = models.CharField(max_length=300)
    Division = models.CharField(max_length=300)
    GST_No = models.CharField(max_length=300)
    ECC_No = models.CharField(max_length=300)
    PAN_No = models.CharField(max_length=10)
    CIN_NO = models.CharField(max_length=21)
    Import_Export_Date = models.DateField(null=True)  # Example of nullable DateField
    ARN_Date = models.DateField(null=True)  # Example of nullable DateField
    LUT_Date = models.DateField(null=True)  # Example of nullable DateField
    login_logo=models.ImageField(upload_to="my_picture1")
    home_logo=models.ImageField(upload_to="my_picture2")
    company_logo=models.ImageField(upload_to="my_picture3")
    Tuv_logo=models.ImageField(upload_to="my_picture4")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class Candidate(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        parent_link=True,
        related_name='candidate',
    )
    name = models.CharField(max_length=256, null=True, blank=True)
    mobile = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _('Candidate')
        verbose_name_plural = _('Candidates')



# Admin Model: Erp_admin
class AdminModel(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        parent_link=True,
        related_name='adminmodel',
    )
    email_id = models.EmailField(unique=True)

    class Meta:
        verbose_name = _('AdminModel')
        verbose_name_plural = _('adminmodels')


class UserAccess(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        parent_link=True,
        related_name='UserAccess',
    )
    mobile_no = models.CharField(max_length=15)
    plant_name = models.CharField(max_length=100)
    is_store_permitted = models.BooleanField(default=False)
    is_purchase_permitted = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('UserAccess')
        verbose_name_plural = _('UserAccess')

    def custom_method_for_vendor(self):
        # Add any custom logic here
        pass