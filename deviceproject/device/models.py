from djongo import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from location.models import Location
from django.utils import timezone
from datetime import datetime
import uuid
import random
import rsa
import base64
import qrcode
from django.core.files.storage import FileSystemStorage
from PIL import Image,ImageDraw
import PIL
from io import BytesIO
from django.core.files import File
from location.models import Location


class Device(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    device_name=models.CharField(max_length=150,blank=False)
    device_type=models.CharField(max_length=150,blank=False)
    serial_number  = models.CharField(max_length=100,null=True,blank=True,unique=True)
    mac_address  = models.CharField(max_length=100,null=True,blank=True,unique=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,blank=True)
    public_key = models.CharField(max_length=2000,null=True,blank=True,unique=True)
    private_key = models.CharField(max_length=2000,null=True,blank=True,unique=True)
    last_seen=models.DateTimeField(default=timezone.now)
    is_active=models.BooleanField(max_length=100,default=False)
    authorization_token=models.UUIDField(unique=True,default=uuid.uuid4,editable=False)
    authentication_token=models.UUIDField(unique=True,default=uuid.uuid4,editable=False)
    qr_code_token=models.CharField(max_length=150,blank=False)

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'