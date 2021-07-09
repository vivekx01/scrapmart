from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import city,locality
from shopmanagement.models import searchdb

# Create your views here.
def searchview(request):
    #code to fetch search query and show search results page
    if not request.user.is_authenticated:
        messages.add_message(request,messages.INFO,"Please Login first")
        return redirect('userloginpage')
    else:
        res=False
        context={'cities':city.objects.all(),'res':res}
        return render (request,"search.html",context)

def load_localities(request):
    cityfetch = request.GET.get('city')
    cityget= city.objects.get(name=cityfetch)
    localities = locality.objects.filter(city_id=cityget.id).order_by('name')
    context={'localities':localities}
    return render(request, 'locality_dropdown_list_options.html',context)

def searchresult(request):
    #code for accepting search input from user and displaying results
    try:
        city_fetch=request.POST['city']
        locality=request.POST['locality']
        results=searchdb.objects.filter(city=city_fetch,locality=locality,is_verified=True)
        if results.exists():
            res=True
            context={'results': results,'cities':city.objects.all(),'res':res}
            return render(request,"search.html",context)
        else:
            des=True
            context={'cities':city.objects.all(),'des':des}
            return render(request,"search.html",context)
    except Exception as e:
        context={'cities':city.objects.all()}
        return render(request,"search.html",context)

def searchprofile(request,profilepk):
    #loading the profile page of a shop
    profileresult=searchdb.objects.filter(id=profilepk)
    context={'results':profileresult}
    return render(request,"searchprofile.html",context)

