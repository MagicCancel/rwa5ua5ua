from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):

    #user
    UserData = models.OneToOneField(User, related_name="Account")
	
    #name
    firstName = models.TextField()
    middleName = models.TextField()
    lastName = models.TextField()
            
    #Date of birth
            
    #social security number
    ssn = models.DecimalField(max_digits=9, decimal_places=0)
            
    #money put in
    fund = models.DecimalField(default=0, max_digits=9, decimal_places=2)	

    #zip code
    zipCode = models.DecimalField(max_digits=5, decimal_places=0)

    def __srt__(self):
        return self.UserData.username
    #end def

#end class


class StockRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(UserAccount, related_name="stock_creator_set")
    company = models.TextField()
    amount = models.DecimalField(default=0, max_digits=9, decimal_places=2)

    #mirroring info
    isFromMirror = models.BooleanField(default = False)
    mirrorSold = models.BooleanField(default = False)
    mirrorEntry = models.ForeignKey('self', related_name="mirror_set", null=True, blank=True, default = None)
#end class

class Follow(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(UserAccount, related_name="follow_creator_set")
    following = models.ForeignKey(UserAccount, related_name="follow_set")

    def __srt__(self):
        return self.creator.username
    #end def
    
#end class

class Mirror(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(UserAccount, related_name="mirror_creator_set")
    mirroring = models.ForeignKey(UserAccount, related_name="mirror_set")
    fund = models.DecimalField(default=0, max_digits=9, decimal_places=2)
#end class

############################################################################## FORMS

class StockInvestForm(models.Model):
    company = models.TextField()
    amount = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    creatorEmail = models.TextField()
#end class

class StockSellingForm(models.Model):
    userEmail = models.TextField()
    index = models.DecimalField(default=0, max_digits=9, decimal_places=0)
#end class

class SignupForm(models.Model):
    userName = models.TextField()
    email = models.TextField()
    password = models.TextField()
    firstName = models.TextField()
    middleName = models.TextField()
    lastName = models.TextField()
    ssn = models.DecimalField(max_digits=9, decimal_places=0)
    zipCode = models.DecimalField(max_digits=5, decimal_places=0)

    def __srt__(self):
        return self.UserData.username
    #end def
#end class

class FollowForm(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creatorEmail = models.TextField()
    followingEmail = models.TextField()
#end class

class MirrorForm(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creatorEmail = models.TextField()
    mirroringEmail = models.TextField()
    fund = models.DecimalField(default=0, max_digits=9, decimal_places=2)
#end class


class FundUpdateForm(models.Model):
    userEmail = models.TextField()
    newFund = models.DecimalField(default=0, max_digits=9, decimal_places=2)
#end class





