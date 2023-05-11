from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
       return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix.cloudantnosqldb.appdomain.cloud/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        
        url = "https://b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix.cloudantnosqldb.appdomain.cloud/get-dealership"
        dealer = get_dealer_by_id_from_cf(url, id=id)
        context["dealer"] = dealer
        
        url = "https://b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix.cloudantnosqldb.appdomain.cloud/get-review"
        reviews = get_dealer_reviews_from_cf(url, id=id)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/index.html', context)

# Create a `add_review` view to submit a review
def add_review(request, id):
    
    if request.method == 'GET' or not request.user.is_authenticated:
        context = {}    
        return render(request, 'djangoapp/add_review.html', context)
    
    elif request.method == 'POST':
        
        payload = dict()

        url = "https://b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix.cloudantnosqldb.appdomain.cloud/get-dealership"
        dealer = get_dealer_by_id_from_cf(url, id=id)
        
        payload["dealership"] = dealer
        payload["name"] = request.POST["name"]
        payload["purchase"] = request.POST["purchase"]
        payload["review"] = request.POST["review"]
        payload["purchase_date"] = request.POST["purchase_date"]
        payload["car_make"] = request.POST["car_make"]
        payload["car_model"] = request.POST["car_model"]
        payload["car_year"] = request.POST["car_year"]
        payload["id"] = request.POST["id"]
        
        return redirect("djangoapp:dealer_details", id=id)


