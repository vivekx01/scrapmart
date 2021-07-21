"""Scrapmart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.adminloginview),
    path('authenticate/',views.authenticateadmin),
    path('homepage/',views.adminhomepageview),
    path('logout/',views.logoutadmin),
    path('addshop/',views.adminaddshopview),
    path('addlocations/',views.adminlocations),
    path('userqueries/',views.userqueries),
    path('listingrequests/',views.adminrequests,name="approvalrequests"),
    path('listingapprove/<int:listingpk>/',views.listingapprove),
    path('listingreject/,<int:listingpk>/',views.listingreject),
    path('addlocation/',views.addlocation),
    path('shopdetailsubmit/',views.adminaddshops),
    path('deletelocality/<int:deletepk>/',views.deletelocality),
    path('deletecity/<int:deletepk>/',views.deletecity),
    path('responded/<int:querypk>/',views.queryresponded),
    path('deletequery/<int:querypk>/',views.querydelete),
    path('localityget/',views.fetchlocalities),
    path('usermanage/',views.usermanageview),
    path('usersearch/',views.usersearch),
    path('userdisable/<int:userpk>/',views.userdisable),
    path('userdelete/<int:userpk>/',views.userdelete),
    path('userenable/<int:userpk>/',views.userenable),
    path('scrapmartmailer/',views.adminmailerview),
    path('mailsend/',views.adminmailsend),
    path('searchmanage/',views.searchmanageview),
    path('searchmanage/searchresult/',views.searchresult),
    path('searchmanage/profile/<int:profilepk>/',views.searchprofile),
    path('searchmanage/disable/<int:profilepk>/',views.shopdisable),
    path('searchmanage/enable/<int:profilepk>/',views.shopenable),
    path('searchmanage/delete/<int:profilepk>/',views.shopdelete),
]
