from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="Home page"),
    path('gencertificate',views.writeonimage,name="bulk creator"),
    path('readdata',views.readata,name="Read from csv"),
]
