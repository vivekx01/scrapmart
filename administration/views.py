from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from usermanagement.models import User
from django.contrib import messages
from usermanagement.models import userinfo
from searchconsole.models import city,locality
from shopmanagement.models import searchdb
from main.models import userquery
from django.core.mail import send_mail
from Scrapmart import settings

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

def adminrequests(request):
    #code to retrieve the admin panel approval requests page
    if not request.user.is_authenticated:
        return render(request,'adminlogin.html')
    else:
        if searchdb.objects.filter(is_verified=False).exists():
            requests=searchdb.objects.filter(is_verified=False)
            res=True
        else:
            requests=searchdb.objects.filter(is_verified=False)
            res=False
        context={'requests':requests,'res':res}
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
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    queries=userquery.objects.filter(status=False)
    context={'queries':queries}
    return render(request,"userqueries.html",context)

def adminaddshopview(request):
    #code to render admin panel add shop function
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
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
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    context={'cities':city.objects.all(),'localities':locality.objects.all()}
    return render(request,'editlocations.html',context)

def fetchlocalities(request):
    #code to load localities in the table 
    cityid=request.POST['city']
    localityget=locality.objects.filter(city_id=cityid)
    citydata=city.objects.get(id=cityid)
    res=True
    context={'cities':city.objects.all(),'localities':localityget,'res':res,'cityname':citydata.name}
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
    messages.add_message(request,messages.INFO,'Deleted Successfully')
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

def usermanageview(request):
    #renders the user management page in the admin panel
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    return render (request,'usermanage.html')

def usersearch(request):
    #accepts search query and retrieves user information
    username=request.POST['username']
    if User.objects.filter(username=username).exists():
        userauthinfo= User.objects.filter(username=username)
        userauthget= User.objects.get(username=username)
        userotherinfo= userinfo.objects.filter(user_id=userauthget.id)
        if userauthget.is_active==False:
            dis=True
        else:
            dis=False
        res=True
        context={'authinfo':userauthinfo,'otherinfo':userotherinfo,'res':res,'dis':dis}
        return render(request,'usermanage.html',context)
    else:
        des=True
        context={'des':des}
        return render(request,'usermanage.html',context)

def userdelete(request,userpk):
    #deletes account and all other information related to the account
    user= User.objects.get(id=userpk)
    if userinfo.objects.filter(user_id=userpk).exists():
        extinfo= userinfo.objects.get(user_id=userpk)
        extinfo.delete()
    if searchdb.objects.filter(user_id=userpk).exists():
        shopinfo= searchdb.objects.get(user_id=userpk)
        shopinfo.delete()
    user.delete()
    messages.add_message(request,messages.INFO,"User data wiped Successfully")
    return render(request,'usermanage.html')

def userdisable(request,userpk):
    #disables the user account
    user= User.objects.get(id=userpk)
    user.is_active=False
    user.save()
    userauthinfo= User.objects.filter(id=userpk)
    userauthget= User.objects.get(id=userpk)
    userotherinfo= userinfo.objects.filter(user_id=userauthget.id)
    if userauthget.is_active==False:
        dis=True
    else:
        dis=False
    res=True
    context={'authinfo':userauthinfo,'otherinfo':userotherinfo,'res':res,'dis':dis}
    messages.add_message(request,messages.INFO,"Account Disabled Successfully")
    return render(request,'usermanage.html',context)

def userenable(request,userpk):
    #enables the user account
    user= User.objects.get(id=userpk)
    user.is_active=True
    user.save()
    userauthinfo= User.objects.filter(id=userpk)
    userauthget= User.objects.get(id=userpk)
    userotherinfo= userinfo.objects.filter(user_id=userauthget.id)
    if userauthget.is_active==False:
        dis=True
    else:
        dis=False
    res=True
    context={'authinfo':userauthinfo,'otherinfo':userotherinfo,'res':res,'dis':dis}
    messages.add_message(request,messages.INFO,"Account Enabled Successfully")
    return render(request,'usermanage.html',context)

def adminmailerview(request):
    #loads the admin mailer daemon page
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    return render(request,'mailer.html')

def adminmailsend(request):
    #fetches data entered by admin and emails the designated receiver using mailer
    email=request.POST['email']
    subject=request.POST['subject']
    message=request.POST['message']
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    messages.add_message(request,messages.SUCCESS,"Message Sent Successfully")
    return redirect('/admin/scrapmartmailer/')

def searchmanageview(request):
    #renders search manage page for search database management
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,"Please Login first")
        return redirect('/admin/login/')
    else:
        res=False
        context={'cities':city.objects.all(),'res':res}
        return render (request,"searchmanage.html",context)

def searchresult(request):
    #code for accepting search input from user and displaying results
    try:
        city_fetch=request.POST['city']
        locality=request.POST['locality']
        results=searchdb.objects.filter(city=city_fetch,locality=locality)
        if results.exists():
            res=True
            context={'results': results,'cities':city.objects.all(),'res':res}
            return render(request,"searchmanage.html",context)
        else:
            des=True
            context={'cities':city.objects.all(),'des':des}
            return render(request,"searchmanage.html",context)
    except Exception as e:
        context={'cities':city.objects.all()}
        return render(request,"searchmanage.html",context)

def searchprofile(request,profilepk):
    #loading the profile page of a shop
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    profileresult=searchdb.objects.filter(id=profilepk)
    context={'results':profileresult}
    return render(request,"searchmanageprofile.html",context)

def shopdelete(request,profilepk):
    s= searchdb.objects.get(id=profilepk)
    s.delete()
    messages.add_message(request,messages.INFO,"Deleted successfully")
    return redirect('/admin/searchmanage/')

def shopenable(request,profilepk):
    s= searchdb.objects.get(id=profilepk)
    s.is_verified=True
    s.save()
    messages.add_message(request,messages.INFO,"Enabled successfully")
    return redirect(request.META['HTTP_REFERER'])

def shopdisable(request,profilepk):
    s= searchdb.objects.get(id=profilepk)
    s.is_verified=False
    s.save()
    messages.add_message(request,messages.INFO,"Disabled successfully")
    return redirect(request.META['HTTP_REFERER'])









