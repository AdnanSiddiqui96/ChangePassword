from django.shortcuts import render
import datetime
from datetime import datetime, timedelta
import jwt
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F, Q
from django.http import HttpResponse
from rest_framework import status
from django.shortcuts import render
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import generics
import api.usable as uc
from django.conf import settings
from .models import *
import random
from .models import Account, UserPassword
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.hashers import check_password, make_password


# User_Account/API

class Register(APIView):
    def get(self, request):

        # saloon_name=F('saloon_id__saloon_name')
        data = Account.objects.values('uid','firstname','lastname','email','contact',Role=F('role_id__role'))
        if  data:
            return Response({"status":True,'All_Users':data,})
        else:
            return Response({"status":True,'Msg':'data not found'})


    def post (self,request):
        requireFields = ['firstname','lastname','email','password','contact']
        validator = uc.keyValidation(True,True,request.data,requireFields)

        if validator:
            return Response(validator,status = 200)

        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            contact = request.data.get('contact')
            role_id = request.data.get('role_id')

            objrole = Role.objects.filter(role = 'admin').first()

            if uc.checkemailforamt(email):
                if not uc.passwordLengthValidator(password):
                    return Response({"status":False, "message":"password should not be than 8 or greater than 20"})

                checkemail=Account.objects.filter(email=email).first()
                if checkemail:
                    return Response({"status":False, "message":"Email already exists"})

                checkphone=Account.objects.filter(contact=contact).first()
                if checkphone:
                    return Response({"status":False, "message":"phone no already existsplease try different number"})

                data = Account(firstname = firstname, lastname = lastname, email=email, password=handler.hash(password), contact=contact, role_id=objrole)

                data.save()

                return Response({"status":True,"message":"Account Created Successfully"})
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"})




class login(APIView):
     def post(self,request):
         requireFields = ['email','password']
         validator = uc.keyValidation(True,True,request.data,requireFields)

         if validator:
            return Response(validator,status = 200)

         else:
              email = request.data.get('email')
              password = request.data.get('password')
              fetchAccount = Account.objects.filter(email=email).first()
              if fetchAccount:
                  if handler.verify(password,fetchAccount.password):
                     if fetchAccount.role_id.role == 'admin':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname,
                               'exp': datetime.utcnow() + timedelta(days=22),
                          }
                        access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'contact':fetchAccount.contact,'email':fetchAccount.email, 'Login_As':str(fetchAccount.role_id)}

                        whitelistToken(token = access_token, user_agent = request.META['HTTP_USER_AGENT'],created_at = datetime.now(), role_id=fetchAccount).save()

                        return Response({"status":True,"message":"Login Successfully","token":access_token,"admindata":data})

                     else:
                        return Response({"status":False,"message":"Unable to login"})
                  else:
                     return Response({"status":False,"message":"Invalid Creadientialsl"})
              else:
                  return Response({"status":False,"message":"Unable to login"})






class AdminRegister(APIView):


    def get(self, request):        
        admin_users = Account.objects.filter(role_id__role ="admin").values('firstname', 'lastname', 'email',Role=F('role_id__role'))

        if admin_users:
            return Response({"status": True, 'Admin_Roles': admin_users})
        else:
            return Response({"status": True, 'Msg': 'No admin roles found'})


    def post (self,request):
        requireFields = ['firstname','lastname','email','password','contact']
        validator = uc.keyValidation(True,True,request.data,requireFields)

        if validator:
            return Response(validator,status = 200)

        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            contact = request.data.get('contact')
            role_id = request.data.get('role_id')

            objrole = Role.objects.filter(role = 'admin').first()

            if uc.checkemailforamt(email):
                if not uc.passwordLengthValidator(password):
                    return Response({"status":False, "message":"password should not be than 8 or greater than 20"})

                checkemail=Account.objects.filter(email=email).first()
                if checkemail:
                    return Response({"status":False, "message":"Email already exists"})

                checkphone=Account.objects.filter(contact=contact).first()
                if checkphone:
                    return Response({"status":False, "message":"phone no already existsplease try different number"})

                data = Account(firstname = firstname, lastname = lastname, email=email, password=handler.hash(password), contact=contact, role_id=objrole)

                data.save()

                return Response({"status":True,"message":"Account Created Successfully"})
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"})



class ChangePassword(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        new_password = request.data.get('new_password', '')

        # Fetch the account based on the email
        account = get_object_or_404(Account, email=email)

        # Fetch the six most recent passwords for the account
        recent_passwords = UserPassword.objects.filter(account_id=account).order_by('-created_at')[:6]

        # Check if the new password matches any of the recent passwords
        if any(check_password(new_password, password.password) for password in recent_passwords):
            # Get the last 6 passwords from the database
            last_six_passwords = [password.password for password in recent_passwords]

            return Response({
                "status": False,
                "message": "Cannot use a previously used password",
                "last_six_passwords": last_six_passwords
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update the password in the UserPassword table
        user_password = UserPassword.objects.create(password=make_password(new_password), account_id=account)

        # Update the password in the Account table using your custom handler
        account.password = make_password(new_password)
        account.no_of_wrong_attempts = 0  # Reset the wrong attempts counter
        account.save()

        return Response({"status": True, "message": "Password changed successfully"}, status=status.HTTP_200_OK)


