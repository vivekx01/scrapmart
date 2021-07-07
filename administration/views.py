from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from usermanagement.models import userinfo
from searchconsole.models import city,locality
from shopmanagement.models import searchdb
from main.models import userquery

# Create your views here.
def adminloginview(request):
    #loads the login page for admin
    if not request.user.is_authenticated:
        return render(request,'adminlogin.html')
    elif request.user.is_authenticated and request.user.is_superuser==False:
        return redirect("/user/homepage/")
    else:
        return render(request,"adminhomepage.html")

def adminhomepageview(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    return render (request,"adminhomepage.html")
        
def authenticateadmin(request):
    #function to authenticate admin login
    username=request.POST['username']
    password=request.POST['password']
    #authentication
    user = authenticate(username=username, password=password)
    #if the user exists
    if user is not None and user.is_superuser==True:
        #login code
        login(request,user)
        return redirect('/admin/homepage/')
    #if the user does not exist
    elif user is None:
        messages.add_message(request,messages.ERROR,"Invalid credentials")
        return redirect ('/admin/login/')
    else:
        messages.add_message(request,messages.ERROR,"Superuser account needed")
        return redirect ('/admin/login/')

def logoutadmin(request):
    #code for logout from admin panel
    logout(request)
    return redirect('/admin/login')

######code to be fixed yet starts here#########

def adminrequests(request):
    #code to retrieve the admin panel approval requests page
    requests=searchdb.objects.filter(is_verified=False)
    context={'requests':requests}
    return render(request,"approvalrequests.html",context)

def listingapprove(request,listingpk):
    #Approving listing request and adding data to search db
    u=searchdb.objects.get(id=listingpk)
    u.is_verified=True
    u.save()
    return redirect('approvalrequests')

def listingreject(request,listingpk):
    #Rejecting a listing request in order to contact user
    u=searchdb.objects.filter(id=listingpk)[0]
    u.is_verifed=False
    u.save()
    return redirect('approvalrequests')

def userqueries(request):
    #code to retrieve the user queries for admin
    queries=userquery.objects.filter(status=False)
    context={'queries':queries}
    return render(request,"userqueries.html",context)

def adminaddshopview(request):
    #code to render admin panel add shop function
    context={'cities':city.objects.all()}
    return render(request,'adminaddshop.html',context)

def adminaddshops(request):
    #code to add the shop data from admin side to the search db
    username=request.POST['username']
    city_fetch=request.POST['city']
    locality_fetch=request.POST['locality']
    shopname=request.POST['shopname']
    shopaddress=request.POST['shopaddress']
    shopcontact=request.POST['shopcontact']
    shopimage=request.FILES['img']
    #if the user has already submitted a request
    if searchdb.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"User has already submitted their request please check the listing approvals.")
        return render (request,'adminaddshop.html')
    else:
        u=searchdb(username=username,shopname=shopname,city=city_fetch,locality=locality_fetch,shopaddress=shopaddress,shopcontact=shopcontact,shopimage=shopimage,is_verified=True)
        u.save()
        messages.add_message(request,messages.SUCCESS,"Shop added successfully")
        return render (request,'addminaddshop.html')

def adminlocations(request):
    #code to render the edit locations page from the admin panel
    context={'cities':city.objects.all(),'localities':locality.objects.all()}
    return render(request,'editlocations.html',context)

def addlocation(request):
    #code to add the city and locality to their respective databases
    city_fetch=request.POST['city']
    locality_fetch=request.POST['locality']
    #if the city already exists
    if city.objects.filter(name=city_fetch).exists():
        if locality.objects.filter(name=locality_fetch).exists():
            #code that will run if both city and locality already exist
            messages.add_message(request,messages.ERROR,"City and locality already exist")
            return redirect('/admin/addlocations')
        else:
            #code that will run if the city exists but locality does not exist
            cityget=city.objects.get(name=city_fetch)
            locality(name=locality_fetch,city_id=cityget.id).save()
            messages.add_message(request,messages.SUCCESS,"Locality Added successfully")
            return redirect('/admin/addlocations')
    else:
        #code that will run if both don't exist
        city(name=city_fetch).save()
        cityget=city.objects.get(name=city_fetch)
        locality(name=locality_fetch,city_id=cityget.id).save()
        messages.add_message(request,messages.SUCCESS,"City and Locality Added successfully")
        return redirect ('/admin/addlocations')

def deletelocality(request,deletepk):
    #code to delete a city or locality
    localitydb=locality.objects.get(id=deletepk)
    localitydb.delete()
    context={'cities':city.objects.all(),'localities':locality.objects.all()}
    return render(request,"editlocations.html",context)

def deletecity(request,deletepk):
    #code to delete a city or locality
    citydb=locality.objects.get(id=deletepk)
    citydb.delete()
    context={'cities':city.objects.all(),'localities':locality.objects.all()}
    return render(request,"editlocations.html",context)

def queryresponded(request,querypk):
    #when the admin responds to a query and marks it responded
    q=userquery.objects.get(id=querypk)
    q.status=True
    q.save()
    return redirect('/admin/userqueries/')

def querydelete(request,querypk):
    #if the admin wishes to delete a query
    q=userquery.objects.get(id=querypk)
    q.delete()
    return redirect('/admin/userqueries/')



