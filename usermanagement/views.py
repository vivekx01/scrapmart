from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import userinfo
from usermanagement.models import User
from django.contrib import messages

# Create your views here.
def userlogout(request):
    #code for logout from user homepage
    logout(request)
    return render(request,'homepage.html')

def userhomepageview(request):
    #loading the user homepage
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    return render (request,"userhomepage.html")

def profilepage(request):
    #code to load the profile page of the user
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    userid=request.user.id
    username=request.user.username
    firstname=request.user.first_name
    lastname=request.user.last_name
    email=request.user.email
    datejoined=request.user.date_joined
    data=userinfo.objects.filter(user_id=userid)
    context={'username':username,'firstname':firstname,'lastname':lastname,'email':email,'datejoined':datejoined,'datas':data}
    return render(request,"profilepage.html",context)

def editprofileview(request):
    #code to load edit profile page
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    userid=request.user.id
    username=request.user.username
    firstname=request.user.first_name
    lastname=request.user.last_name
    email=request.user.email
    datejoined=request.user.date_joined
    data=userinfo.objects.filter(user_id=userid)
    context={'username':username,'firstname':firstname,'lastname':lastname,'email':email,'datejoined':datejoined,'datas':data,'userid':userid}
    return render (request,'editprofile.html',context)

def profilesave(request,userpk):
    #code to save the changes to the profile after data submission
    firstnameget=request.POST['firstname']
    lastnameget= request.POST['lastname']
    phoneget= request.POST['phone']
    securityquestion= request.POST['securityquestion']
    securityanswer= request.POST['securityanswer']
    u= User.objects.get(id=userpk)
    u.first_name= firstnameget
    u.last_name= lastnameget
    u.save()
    ext=userinfo.objects.get(user_id=userpk)
    ext.phone=phoneget
    ext.securityquestion=securityquestion
    ext.securityanswer=securityanswer
    ext.save()
    messages.add_message(request,messages.INFO,"Profile updated Successfully")
    return redirect ('/user/profile/')
