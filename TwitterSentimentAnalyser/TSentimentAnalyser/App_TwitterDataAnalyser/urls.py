from django.urls import path
from . import views
from App_TwitterTrends.views import trends_form_view

urlpatterns = [
    path('', views.home, name ="home-page"),
    path('contact.html', views.contact, name="contact")
]
