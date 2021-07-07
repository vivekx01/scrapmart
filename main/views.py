from django.shortcuts import render,redirect
from .models import userquery
from django.contrib.auth.models import User
from django.contrib import messages


def hompepageview(request):
    #loads the homepage or userhomepage
    if not request.user.is_authenticated:
        return render(request,'homepage.html')
    else:
        return render(request,"userhomepage.html")
def faqview(request):
    #loads the faq page
    return render (request,"faq.html")

def aboutandcontactview(request):
    #loads the about page
    return render (request,"about.html")

def contactview(request):
    #loads the contact us page for user to submit queries
    return render(request,"contactpage.html")
def querysubmit(request):
    #accept user query and add it to the query database
    email=request.POST['email']
    username=request.POST['username']
    query=request.POST['query']
    if User.objects.filter(username=username,email=email).exists():
        #if the user already has a query pending
        if userquery.objects.filter(username=username,email=email,status=False).exists():
            messages.add_message(request,messages.INFO,"You have already submitted a query")
            return redirect('/contactus/')
        #if the user is submitting a new query
        else:
            userquery(username=username,email=email,query=query).save()
            messages.add_message(request,messages.INFO,"Your query has been submitted.")
            return redirect('/contactus/')
    else:
        messages.add_message(request,messages.INFO,"Account not found")
        return redirect('/contactus/')