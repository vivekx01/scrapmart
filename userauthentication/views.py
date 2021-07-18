from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from usermanagement.models import userinfo
from django.core.mail import send_mail
from Scrapmart import settings

from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator

# Create your views here.
def userloginview(request):
    #loads the user login page
    if request.user.is_authenticated:
        return redirect('/user/homepage/')
    return render (request,"userlogin.html")

def signupview(request):
    #code to render the signup page
    return render (request,"signup.html")

def resetpasswordview(request):
    #code for loading password reset page
    return render(request,"resetpassword.html")

def userauthenticate(request):
    #authenticating the user login
    username=request.POST['username']
    password=request.POST['password']
    #if user exists
    if User.objects.filter(username=username).exists():
        u=User.objects.get(username=username)
        if u.is_active==False:
            messages.add_message(request,messages.ERROR,"Account is not active.")
            return redirect('/user/auth/login/')
        else:
            try:
                user= authenticate(username=username,password=password)
                login(request,user)
                return redirect('/user/homepage/')
            except Exception as e:
                messages.add_message(request,messages.ERROR,"Invalid credentials")
                return redirect('userloginpage')
                   
    #if user does not exist
    else:
        user= authenticate(username=username,password=password)
        if user is None:
            messages.add_message(request,messages.ERROR,"Invalid credentials")
            return redirect('userloginpage')
        
def signup(request):
    #code for adding user to the database
    firstname=request.POST['firstname']
    lastname=request.POST['lastname']
    username=request.POST['username']
    password=request.POST['password']
    email=request.POST['email']
    dob=request.POST['dob']
    phone=request.POST['phone']
    securityquestion=request.POST['securityquestion']
    securityanswer=request.POST['securityanswer']
    #if the user already exists or username is taken
    if User.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"Username taken")
        return redirect ('/user/auth/signup')
    elif User.objects.filter(username=username).exists():
        messages.add_message(request,messages.ERROR,"User already exists")
        return redirect ('/user/auth/signup')
    #if user does not exist
    else:
        #creating user and setting the account to inactive
        user=User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email)
        user.is_active=False
        user.save()
        userget=User.objects.get(username=username)
        userinfo(user_id=userget.id,dob=dob,phone=phone,securityquestion=securityquestion,securityanswer=securityanswer).save()
        #generating a verification token
        uidb64= urlsafe_base64_encode(force_bytes(user.pk))  #encoding user's id
        domain = get_current_site(request).domain  #fetching the current domain on which the application is running
        link= reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)}) #generating a hash value for the token
        activate_url='http://'+domain+link #appending all the parts of the generated token
        #Sending the verification token to user's email ID
        subject = 'Activate your Account'
        message = 'Hi ' + user.username +"\n"+ " Please use the link for verification:\n " + activate_url
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
        messages.add_message(request,messages.SUCCESS,"Account Created. Please check your email for verification")
        return redirect('/user/auth/login/')
        
def verificationview(request, uidb64, token):
    try:
        id= force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=id)
        if not token_generator.check_token(user,token):
            messages.add_message(request,messages.INFO,"Account already activated")
            return redirect('/user/auth/login/')

        if user.is_active:
            return redirect('/user/auth/login/')
        user.is_active=True
        user.save()
        messages.add_message(request,messages.SUCCESS,"Account Successfully Activated! You can now Login.")
        return redirect('/user/auth/login/')
    except Exception as ex:
        pass
    return redirect('/user/auth/login/')

def reset(request):
    #code for resetting the password after receiving the form
    username=request.POST['username']
    new_password=request.POST['password']
    question=request.POST['securityquestion']
    answer=request.POST['securityanswer']
    if User.objects.filter(username=username).exists():
        authinfo=User.objects.get(username=username)
        if authinfo.is_superuser==True:
            messages.add_message(request,messages.ERROR,"Oops! Something is not right")
            return redirect('/user/auth/accountrecovery/')
        uinfo=userinfo.objects.get(user_id=authinfo.id)
        if uinfo.securityquestion==question and uinfo.securityanswer==answer and authinfo.is_superuser==False:
            authinfo.set_password(new_password)
            authinfo.save()
            messages.add_message(request,messages.INFO,"Password Changed Successfully")
            return redirect('/user/auth/accountrecovery/')
        
        else:
            messages.add_message(request,messages.ERROR,"Invalid Credentials entered")
            return redirect('/user/auth/accountrecovery/')
    else:
        messages.add_message(request,messages.ERROR,"User does not exist")
        return redirect('/user/auth/accountrecovery/')