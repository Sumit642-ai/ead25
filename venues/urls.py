from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name="home"),
    path('ead/<str:city>',views.events,name="ead"),
    path('lsm/<str:lsmcity>',views.lsmevent,name="lsm"),
    path('about/',views.about,name="about"),
    path('speakers/',views.speakers,name="speakers"),
    path('contact/',views.contact,name="contact"),
    path('associations/',views.associations,name="associations"),
]


