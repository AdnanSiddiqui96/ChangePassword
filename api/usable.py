import re
from api.models import *
from rest_framework import permissions
from rest_framework.exceptions import APIException
from decouple import config
import jwt


PAYPAL_CLIENT_ID = "AZE62TQ7afmHFj_MpXeoFWWCAT66-cQ-0VFSHDg67yVMyjy6sTmX_4WQjqLrJWskW9vmzaUeqMEisTHT"
PAYPAL_CLIENT_SECRET = "EGjsR4JHp2sthxQydvctUG6p-DBdV5Hq8PFy9Vy_wvjCFk35L-rZLolfSPb9YFYrOZV-86oXAnGsO9kq"

def checkemailforamt(email):
    emailregix = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.match(emailregix, email)):

        return True

    else:
       return False

def passwordLengthValidator(passwd):
    if len(passwd) >= 8 and len(passwd) <= 20:
        return True

    else:
        return False

def requireKeys(reqArray,requestData):
    try:
        for j in reqArray:
            if not j in requestData:
                return False

        return True

    except:
        return False


def allfieldsRequired(reqArray,requestData):
    try:
        for j in reqArray:
            if len(requestData[j]) == 0:
                return False


        return True

    except:
        return False

##both keys and required field validation

def keyValidation(keyStatus,reqStatus,requestData,requireFields):
##keys validation
    if keyStatus:
        keysStataus = requireKeys(requireFields,requestData)
        if not keysStataus:
            return {'status':False,'message':f'{requireFields} all keys are required'}

 ##Required field validation
    if reqStatus:
        requiredStatus = allfieldsRequired(requireFields,requestData)
        if not requiredStatus:
            return {'status':False,'message':'All Fields are Required'}




def admin(token):
    try:

        my_token = jwt.decode(token,config('adminkey'), algorithms=["HS256"])
        return my_token

    except jwt.ExpiredSignatureError:
        return False

    except:
        return False


def manager(token):
    try:

        my_token = jwt.decode(token,config('managerkey'), algorithms=["HS256"])
        return my_token

    except jwt.ExpiredSignatureError:
        return False

    except:
        return False



def customer(token):
    try:

        my_token = jwt.decode(token,config('customerkey'), algorithms=["HS256"])
        return my_token

    except jwt.ExpiredSignatureError:
        return False

    except:
        return False


