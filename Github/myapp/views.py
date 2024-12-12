from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from decimal import Decimal
from django.db.models import F

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal


def home(request):
    template = 'myapp/home.html' if request.user.is_authenticated else 'myapp/signin.html'
    return render(request, template)


@login_required(login_url='signin')
def find_bus(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        travel_date = datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()

        bus_list = Bus.objects.filter(
            source=source,
            dest=destination,
            date__year=travel_date.year,
            date__month=travel_date.month,
            date__day=travel_date.day
        )

        if bus_list.exists():
            return render(request, 'myapp/list.html', {'bus_list': bus_list})
        else:
            return render(request, 'myapp/findbus.html', {
                'data': request.POST,
                'error': "No buses available for the selected route and date."
            })
    return render(request, 'myapp/findbus.html')



@login_required(login_url='signin')
def book_bus(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus_id')
        requested_seats = int(request.POST.get('no_seats'))

        try:
            bus = Bus.objects.get(id=bus_id)
            if bus.rem >= requested_seats:
                cost = requested_seats * bus.price
                remaining_seats = bus.rem - requested_seats

                Bus.objects.filter(id=bus_id).update(rem=remaining_seats)
                booking = Book.objects.create(
                    name=request.user.username,
                    email=request.user.email,
                    userid=request.user.id,
                    bus_name=bus.bus_name,
                    source=bus.source,
                    dest=bus.dest,
                    busid=bus.id,
                    price=bus.price,
                    nos=requested_seats,
                    date=bus.date,
                    time=bus.time,
                    status='BOOKED'
                )
                return render(request, 'myapp/bookings.html', {'booking': booking})
            else:
                return render(request, 'myapp/findbus.html', {'error': "Not enough seats available."})
        except Bus.DoesNotExist:
            return render(request, 'myapp/findbus.html', {'error': "Bus not found."})
    return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('bus_id')

        try:
            booking = Book.objects.get(id=booking_id)
            Bus.objects.filter(id=booking.busid).update(rem=F('rem') + booking.nos)
            booking.status = 'CANCELLED'
            booking.nos = 0
            booking.save()
            messages.success(request, "Booking cancelled successfully.")
            return redirect(view_bookings)
        except Book.DoesNotExist:
            return render(request, 'myapp/error.html', {'error': "Booking not found."})
    return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def view_bookings(request):
    user_bookings = Book.objects.filter(userid=request.user.id)
    if user_bookings.exists():
        return render(request, 'myapp/booklist.html', {'bookings': user_bookings})
    return render(request, 'myapp/findbus.html', {'error': "No bookings found."})


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return render(request, 'myapp/thank.html')
        except Exception:
            return render(request, 'myapp/signup.html', {'error': "Invalid credentials."})
    return render(request, 'myapp/signup.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return render(request, 'myapp/success.html', {'user': user})
        return render(request, 'myapp/signin.html', {'error': "Invalid username or password."})
    return render(request, 'myapp/signin.html', {'error': "Please log in to continue."})


def sign_out(request):
    logout(request)
    return render(request, 'myapp/signin.html', {'error': "You have been logged out."})


def success_page(request):
    return render(request, 'myapp/success.html', {'user': request.user})