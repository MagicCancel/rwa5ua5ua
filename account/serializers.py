from rest_framework import serializers
from account.models import *
from django.contrib.auth.models import User



class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'firstName', 'lastName', 'fund', 'zipCode', 'ssn')
    #end meta

#end class

class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRecord
        field = ('creator', 'company', 'created')
    #end meta
#end class


class FollowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        field = ('creator', 'created')
    #end meta
#end class

class MirrorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mirror
        field = ('creator', 'created')
    #end meta
#end class



############################################################


class StockInvestFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInvestForm
        field = ('company', 'creatorEmail', 'amount')
    #end meta
#end class

class SignupFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupForm
        fields = ('userName', 'password', 'email', 'firstName', 'middleName', 'lastName', 'ssn', 'zipCode')
    #end meta
#end class

class FollowFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowForm
        fields = ("creatorEmail", "followingEmail")
    #end meta
#end class
        
class MirrorFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MirrorForm
        fields = ("creatorEmail", "mirroringEmail", "fund")
    #end meta
#end class

class FundUpdateFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundUpdateForm
        fields = ("userEmail", "newFund")
    #end meta
#end class


class StockSellingFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockSellingForm
        fields = ("userEmail", "index")
    #end meta
#end class






