from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('findbus', views.find_bus, name="findbus"),
    path('bookings', views.book_bus, name="bookings"),
    path('cancellings', views.cancel_booking, name="cancellings"),
    path('seebookings', views.view_bookings, name="seebookings"),
    path('signup', views.sign_up, name="signup"),
    path('signin', views.sign_in, name="signin"),
    path('success', views.success_page, name="success"),
    path('signout', views.sign_out, name="signout"),

]
