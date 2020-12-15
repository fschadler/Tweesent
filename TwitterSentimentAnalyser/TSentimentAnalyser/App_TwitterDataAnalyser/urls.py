from django.urls import path
from . import views

urlpatterns = [
   path('', views.Contact, name="Contact"),
   path('', views.FAQ, name="FAQ"),
   path('', views.export, name='export')
]
