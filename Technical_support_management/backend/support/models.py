from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, AbstractUser
from django.conf import settings
from django.core.validators import EmailValidator,validate_email
from django.utils import timezone
# Create your models here.

class CustomManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None,**extra_fields):
        extra_fields.update({'is_staff':True,'is_superuser':True,'is_active':True})

        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser musr have is_superuser=True")
        
        return self.create_user(email,password,**extra_fields)



class CustomUser(AbstractBaseUser):
    email = models.EmailField(validators=[EmailValidator()], max_length=200,unique=True)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = CustomManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False,help_text="only staff has this field true")
    is_superuser = models.BooleanField(default=False,help_text="Only superadmin should have this field true")

    join_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.email}-{self.full_name}"








class TicketType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    statu_choice = (
        ('new','new'),
        ('in progress','in progress'),
        ('complete','complete'),
        ('closed','closed'),
        ('cancelled','cancelled')
    )

    priority_choice = (
        ('low','low'),
        ('medium','medium'),
        ('high','high'),
        ('urgent','urgent')
    )

    title = models.CharField(max_length=300)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="created_ticket")
    assign_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name="assigned_ticket")
    status = models.CharField(max_length=20,choices=statu_choice,default="open")
    priority = models.CharField(max_length=20,choices=priority_choice,default="medium")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    content = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='comment_attachments/',blank=True,null=True)

    def __str__(self):
        return f"comment by {self.user.username}"
    
class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='ticket_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.uploaded_by.username