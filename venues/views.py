from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
# Create your views here.

def home(request):
    venues=EADVenue.objects.all()
    lsmvenues=LSMVenue.objects.all()
    context={'venues':venues,'lsmvenues':lsmvenues}
    return render(request,'static/Home/index.html',context)

def events(request,city):
    city=get_object_or_404(EADCities,city=city)
    venues=EADVenue.objects.filter(city=city)
    speakers=EADSpeakers.objects.filter(city=city)
    context={'venues':venues,'city':city,'speakers':speakers}
    return render(request,'static/Events/events.html',context)

def lsmevent(request,lsmcity):
    lsmcity=get_object_or_404(LSMCities,city=lsmcity)
    lsmvenues=LSMVenue.objects.filter(city=lsmcity)
    lsmspeakers=LSMSpeakers.objects.filter(city=lsmcity)
    context={'city':lsmcity,'venues':lsmvenues,'speakers':lsmspeakers}
    return render(request,'static/Events/lsm.html',context)

def about(request):
    return render(request,'static/About/about-us.html')


def speakers(request):
    return render(request,'static/Speakers/speakers.html')

def contact(request):
    return render(request,'static/Contact/ContactUs.html')

def associations(request):
    return render(request,'static/Associations/our-sponsors.html')



