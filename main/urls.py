from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.hompepageview),
    path('faq/',views.faqview),
    path('about/',views.aboutandcontactview),
    path('contactus/',views.contactview),
    path('querysubmit/',views.querysubmit),
]
