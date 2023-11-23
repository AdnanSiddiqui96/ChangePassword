from django.db import models
import uuid


two = (

    ('monthly','monthly'),
    ('yearly','yearly')
)

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True ,blank=True,null=True)
    class Meta:
        abstract = True

# #Role table
class Role(BaseModel):
        role=models.CharField(max_length=20, default='user')
        def __str__(self):
            return self.role

# # # register table uuit, created date & updated
class Account(BaseModel):
    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    contact = models.CharField(max_length=255, default='')
    Otp = models.IntegerField(default=0)
    OtpCount = models.IntegerField(default=0)
    OtpStatus = models.BooleanField(default=False)
    no_of_attempts_allowed = models.IntegerField(default=3)
    no_of_wrong_attempts = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    role_id = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.email


# # # register table uuit, created date & updated
class UserPassword(BaseModel):
    password = models.TextField(default='')    
    account_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.password




    # Login Data for records
class whitelistToken(models.Model):
    token = models.CharField(max_length=255, default='')
    user_agent = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add='True', blank = True, null = True)
    role_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.token

