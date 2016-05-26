from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import *
from account.serializers import *
from django.contrib.auth.models import User


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
def account_list(request, format=None):
    #List all code snippets, or create a new snippet.
    if request.method == 'GET':
        accounts = UserAccount.objects.all()
        serializer = UserAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SignupFormSerializer(data=request.data)
        if serializer.is_valid():

            #make sure someone isnt using this email or username
            check1 = User.objects.filter(username = serializer.data['userName']).exists()
            check2 = User.objects.filter(email = serializer.data['email']).exists()
            if check1 == True or check2 == True:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #do not make an account

            #first create the user data
            user = User.objects.create(
                username = serializer.data['userName'],
                email = serializer.data['email'],
                password = serializer.data['password'])

            user.save()
            #now create the user account
            uAcccount = UserAccount(UserData = user,
                                    firstName = serializer.data['firstName'],
                                    middleName = serializer.data['middleName'],
                                    lastName = serializer.data['lastName'],
                                    ssn = serializer.data['ssn'],
                                    zipCode = serializer.data['zipCode'])
            uAcccount.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #end if

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #end elif
#end def

@api_view(['GET', 'PUT', 'DELETE'])
def account_detail(request, pk, format=None):
    #Retrieve, update or delete a code snippet.
    try:
        account = UserAccount.objects.get(pk=pk)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserAccountSerializer(account)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserAccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #end elif    
#end def

@api_view(['GET', 'PUT'])
def account_fund_detail(request, pk, format=None):
    #Retrieve, update or delete a code snippet.
    try:
        account = UserAccount.objects.get(pk=pk)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #end try

    if request.method == 'PUT':
        serializer = FundUpdateFormSerializer(data=request.data)
        if serializer.is_valid():
            munny = float(serializer.data["newFund"])
            account.fund = float(account.fund) + munny
            account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #end if
    #end if
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#end def

        
@api_view(['GET', 'POST'])
def stock_detail(request, format=None):
    if request.method == 'GET':
        stocks = StockRecord.objects.all()
        serializer = StockListSerializer(stocks, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = StockInvestFormSerializer(data=request.data)
        if serializer.is_valid():
            #put some shit here
            #grab the account of the investor
            a = User.objects.get(email= serializer.data['creatorEmail']).Account
            b = serializer.data['company']
            cost = serializer.data['amount']
            a.fund = float(a.fund) - float(cost)
            a.save()
            #now make the investment
            creatorStock = StockRecord(creator = a, company = b, amount = cost)
            creatorStock.save()

            #PUT IN THE MIRRORING CODE HERE
            #GET EVERYONE MIRROIRNG THIS GUY
            mirrorSet = a.mirror_set.all()
            #iterate through everyone and have them do the same mirror
            
            for i in mirrorSet:
                person = i.creator
                person.fund = float(person.fund) - float(cost)
                person.save()
                personStock = StockRecord(creator = person, company = b, amount = cost, mirrorEntry = creatorStock)
                personStock.isFromMirror = True
                
                
                personStock.save()
            #end for
            #END MIRRORING CODE

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #end if
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #end elif
#end def

@api_view(['PUT'])
def stock_sell(request, format=None):
    
    if request.method == 'PUT':
        serializer = StockSellingFormSerializer(data=request.data)
        if serializer.is_valid():
            #sell stock
            a = User.objects.get(email= serializer.data['userEmail']).Account
            i = int(serializer.data["index"])
            s = a.stock_creator_set.all()[i]
            #put the money in the stock in the player account
            a.fund = float(a.fund) + float(s.amount)

            #check to see if this had mirrors
            if len(s.mirror_set.all()) > 0:
                for mir in s.mirror_set.all():
                    mir.mirrorSold = True
                    mir.save()
                #end for
                s.mirror_set.clear()
                s.save()
            #end if

            a.save()
            s.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
            #and update mirrors
        #end if
    #end if
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#end def

@api_view(['GET', 'POST'])
def follow_detail(request, format=None):
    if request.method == 'GET':
        follows = Follow.objects.all()
        serializer = FollowListSerializer(follows, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FollowFormSerializer(data=request.data)
        if serializer.is_valid():
            #grab the two accounts
            a = User.objects.get(email= serializer.data['creatorEmail']).Account
            b = User.objects.get(email= serializer.data['followingEmail']).Account
            #now create the follow
            f = Follow(creator = a, following = b) 
            f.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #end if

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #end elif
#end def


@api_view(['GET', 'POST'])
def mirror_detail(request, format=None):
    if request.method == 'GET':
        mirrors = Mirror.objects.all()
        serializer = MirrorListSerializer(mirrors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MirrorFormSerializer(data=request.data)
        if serializer.is_valid():
            #grab the two accounts
            a = User.objects.get(email= serializer.data['creatorEmail']).Account
            b = User.objects.get(email= serializer.data['mirroringEmail']).Account
            munny = serializer.data['fund']
            #now create the mirror
            m = Mirror(creator = a, mirroring = b, fund = munny) 
            m.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #end if

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #end elif
#end def













