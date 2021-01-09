from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from . import serializers
from . import models
from io import BytesIO
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from PIL import Image,ImageDraw
from django.http import Http404,HttpResponse
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
import qrcode
import random
from django.conf import settings
import base64
import hashlib
from django.utils import timezone
from .models import Device
from location.models import Location
import rsa
import base64
import json
import requests
import jwt
import uuid
import datetime
from hashlib import sha512
from string import ascii_uppercase, ascii_lowercase, digits
# {
# "serial_number":"mnbvcxz",
# "mac_address":"lkjhgfdsa",
# "device_name":"qwertyuiop",
# "device_type":"mobile"
# }

# {
#     "authorization_token": "8dd5ec41-0d37-46e4-b25b-cf586bfdf0f9",
#     "authentication_token": "4a264ed7-19a1-4170-a337-7e329bfd2087",
#     "public_key": "PublicKey(7746863096578139315597603842045157779978643507714953398921340501047786923305036259523979108546845634733228019473500365867860442889815489119941423307445347, 65537)"
# }
class Program:
    def key_generator(self):
        (public_key,private_key)=rsa.newkeys(512)
        return public_key,private_key

    def encrytor(self,s,public_key):
        crypto=rsa.encrypt(s.encode('utf-8'),public_key)
        base64text=base64.b64encode(crypto).decode('utf-8')
        return base64text
    
    def decryptor(self,s,private_key):
        crypto=base64.b64decode(s.encode())
        reversed=rsa.decrypt(crypto,private_key).decode('utf-8')
        return reversed

class NewDeviceView(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
            serial_number=request.data.get("serial_number")
            mac_address=request.data.get("mac_address")
            device_name=request.data.get("device_name")
            device_type=request.data.get("device_type")
            print(serial_number)
            # assert None not in [serial_number, mac_address, device_type, device_name]
            try:
                device =Device.objects.get(serial_number=serial_number)
            except:
                device=None
            print(device)
            random_sequence = ascii_uppercase + ascii_lowercase + digits  # added
            new_String="".join(serial_number+''.join(map(str, random.choices(random_sequence,k=9)))+mac_address+r''.join(map(str, random.choices(random_sequence,k=9)))+device_type+''.join(map(str, random.choices(random_sequence,k=9))))
            print("new string",new_String)
            qr_code_token=base64.b64encode(sha512(new_String.encode()).digest()).decode()
            print(qr_code_token)
            if device is not None:
                if device.is_active is False:
                    p=Program()
                    public_key,private_key=p.key_generator()
                    print(public_key,private_key)
                    device.private_key = private_key
                    device.public_key=public_key
                    device.qr_code_token=qr_code_token
                    device.save()
                    content={'qr_code_token':f'{qr_code_token}'}
                    return Response(content,status=status.HTTP_226_IM_USED)
                else:
                    content={'message':f'The device `{device.device_name}` is already active!'}
                    return Response(content,status=status.HTTP_226_IM_USED)
            else:
                print("here")
                p=Program()
                public_key,private_key=p.key_generator()
                print(public_key,private_key)
                print(qr_code_token)
                device= Device.objects.create(serial_number=serial_number,
                                           mac_address=mac_address,
                                           public_key=public_key, 
                                           private_key=private_key,
                                           device_name=device_name,
                                           device_type=device_type,
                                           qr_code_token=qr_code_token)
                device.save()
                content={'qr_code_token':f'{device.qr_code_token}'}
                return Response(content,status=status.HTTP_226_IM_USED)


class DeviceViewset(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializers

class DeviceLastSeenView(APIView):
    def post(self, request):
        authentication_token =request.data.get("authentication_token")
        print(type(authentication_token))
        try:
            device=Device.objects.get(authentication_token=uuid.UUID(authentication_token),is_active=True)
        except:
            device=None
        print(device)
        if device is not None:
            last_seen=device.last_seen
            content={'last_Seen':last_seen}
            return Response(content,status=status.HTTP_226_IM_USED)
        else:
            content={'error':'token is not valid!'}
            return Response(content,status=status.HTTP_226_IM_USED)

class DeviceLastSeenUpdateView(APIView):
    def post(self, request):
        authentication_token =request.data.get("authentication_token")
        try:
            device=Device.objects.get(authentication_token=uuid.UUID(authentication_token),is_active=True)
        except:
            device=None
        if device is not None:
            device.last_seen=datetime.datetime.now()
            content={'message':'device last seeen is updated'}
            return Response(content,status=status.HTTP_226_IM_USED)
        else:
            content={'error':'token is not valid!'}
            return Response(content,status=status.HTTP_226_IM_USED)

class DeviceTokenView(APIView):
    def post(self,request):
        qr_code_token=request.data.get("qr_code_token")
        print(qr_code_token)
        try:
            device=Device.objects.get(qr_code_token=qr_code_token,is_active=False)
        except:
            device=None
        print(device)
        if device is not None:
            device.is_active=True
            device.save()
            content={"Authorization_token":device.authorization_token,
                    "Authentication_token":device.authentication_token,
                    "Public_key":device.public_key
                    }
            return Response(content,status=status.HTTP_226_IM_USED)
        else:
            content={'error':'Authentication Rejected/Information  not sufficient!'}
            return Response(content,status=status.HTTP_226_IM_USED)

class DeviceKeyExchangeView(APIView):
    def post(self,request):
        authentication_token =request.data.get("authentication_token")
        payload=request.data.get("payload")
        try:
            device=Device.objects.filter(authentication_token=authentication_token,is_active=True).first()
        except:
            device=None
        if device is not None:
            base64text=Program.decryptor(payload,device.private_key)
            device_dict=dict(base64text)
            try:
                device=Device.objects.get(serial_number=device_dict.get("serial_number"),mac_address=device_dict.get("mac_address"),authorization_token=device_dict.get("authorization_token"),public_key=device_dict.get("public_key"))
            except:
                device=None
            if device is not None:
                content={"success":"True"}
            else:
                content={"error":"information is not correct!"}
        return Response(content,status=status.HTTP_226_IM_USED)

class DeviceReauthenticateView(APIView):
    def post(self,request):
        authorization_token=request.data.get("authorization_token")
        payload=request.data.get("payload")
        try:
            device=Device.objects.filter(authorization_token=uuid.UUID(authorization_token),is_active=True).first()
        except:
            device=None
        if device is not None:
            base64text=Program.decryptor(payload,device.private_key)
            device_dict=dict(base64text)
            try:
                device=Device.objects.filter(authentication_token=uuid.UUID(device_dict.get("authentication_token")),is_active=True).first()
            except:
                device=None
            if device is not None:
                device.authentication_token=uuid.uuid4
                device.save()
                content={"authentication_token":device.authentication_token}
        else:
            content={"error":"Information not sufficient!"}
        return Response(content,status=status.HTTP_226_IM_USED)

class DeviceDetailsView(APIView):
    def post(self,request):
        authentication_token=request.data.get("authentication_token")
        payload=request.data.get("payload")
        try:
            device=Device.objects.filter(authentication_token=authentication_token,is_active=True).first()
        except:
            device=None
        if device is not None:
            base64text=Program.decryptor(payload,device.private_key)
            device_dict=dict(base64text)
            try:
                device=Device.objects.get(serial_number=device_dict.get("serial_number"),
                mac_address=device_dict.get("mac_address"),
                authorization_token=UUID.uuid(device_dict.get("authorization_token")),
                public_key=device_dict.get("public_key"))
            except:
                device=None
            if device is not None:
                content={"serial_number":device.serial_number,
                "mac_address":device.mac_address,
                "name":device.name,
                "type":device.device_type,
                "services_runnning":"1"}
        else:
            content={"error":"Information not sufficient!"}
        return Response(content,status=status.HTTP_226_IM_USED)