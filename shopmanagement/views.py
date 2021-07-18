from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from searchconsole.models import city
from .models import searchdb
# Create your views here.
def getlistedview(request):
    #code to load listing form
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,"Please Login first")
        return redirect('userloginpage')
    else:
        context={'cities':city.objects.all()}
        return render(request,'getlisted.html',context)

def getlistedformsubmit(request):
    # code to submit the listing request form data for approval in admin panel
    userid=request.user.id
    selectcity=request.POST['city']
    selectlocality=request.POST['locality']
    shopname=request.POST['shopname']
    shopaddress=request.POST['shopaddress']
    shopcontact=request.POST['shopcontact']
    shopimage=request.FILES['img']
    #if the user has already submitted a request
    if searchdb.objects.filter(user_id=userid).exists():
        messages.add_message(request,messages.ERROR,"You have already submitted a request.Please wait while we verify.")
        return redirect ('/user/homepage/')
    else:
        u=searchdb(user_id=userid,shopname=shopname,city=selectcity,locality=selectlocality,shopaddress=shopaddress,shopcontact=shopcontact,shopimage=shopimage)
        u.save()
        messages.add_message(request,messages.SUCCESS,"Your Request Has been submitted")
        return redirect ('/user/homepage/')

def viewshop(request):
    #code to retrieve status page after submission
    userid=request.user.id
    if searchdb.objects.filter(user_id=userid).exists():
        infos=searchdb.objects.filter(user_id=userid)
        context={'infos':infos}
        return render(request,"dealerprofile.html",context)
    else:
        messages.add_message(request,messages.INFO,"Please apply to get listed.")
        return redirect('/shop/getlisted/')

def editdealerprofileview(request):
    #code to render edit dealer profile page
    if not request.user.is_authenticated:
        return render(request,'homepage.html')
    else:
        userid=request.user.id
        infos=searchdb.objects.filter(user_id=userid)
        context={'infos':infos}
        return render(request,"editdealerprofile.html",context)

    

def editdealersave(request):
    #code to save shop details after editing
    userid= request.user.id
    shopname= request.POST['shopname']
    shopaddress= request.POST['shopaddress']
    shopcontact= request.POST['shopcontact']
    s=searchdb.objects.get(user_id=userid)
    s.shopname= shopname
    s.shopaddress= shopaddress
    s.shopcontact= shopcontact
    s.is_verified=False
    s.save()
    messages.add_message(request,messages.INFO,"Details Updated Successfully")
    return redirect('/shop/dealerprofile/')
