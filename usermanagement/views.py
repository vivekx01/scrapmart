from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import userinfo
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
    userid=request.user.id
    username=request.user.username
    firstname=request.user.first_name
    lastname=request.user.last_name
    email=request.user.email
    datejoined=request.user.date_joined
    data=userinfo.objects.filter(user_id=userid)
    context={'username':username,'firstname':firstname,'lastname':lastname,'email':email,'datejoined':datejoined,'datas':data}
    return render(request,"profilepage.html",context)
