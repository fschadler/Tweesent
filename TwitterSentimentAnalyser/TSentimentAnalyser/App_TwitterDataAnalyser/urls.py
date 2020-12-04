from django.urls import path
from . import views
from App_TwitterTrends.views import trends_form_view

urlpatterns = [
   path('', views.Contact, name="Contact"),
]
