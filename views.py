from django.shortcuts import render
from .forms import ListingForm 
from .models import User, Listing, Category 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import User
from django.http import JsonResponse # Add this to your imports at the top
from .models import Listing, Bid # Make sure Bid is import

def index(request):
    # Change 'order_some' to 'order_by'
    listings = Listing.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "auctions/index.html", {
        "listings": listings
    })
    

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
            
    return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
            
        login(request, user)
        return redirect("index")
        
    return render(request, "auctions/register.html") 

def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.current_price = listing.starting_bid
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    
    return render(request, "auctions/create.html", {"form": form})




def listing_detail(request, id):
    listing = Listing.objects.get(pk=id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

def add_bid(request, id):
    # This view will receive JavaScript Fetch requests
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        bid_amount = float(data.get("amount"))
        listing = Listing.objects.get(pk=id)

        # Basic Validation
        if bid_amount <= listing.current_price:
            return JsonResponse({"success": False, "message": "Bid must be higher than current price."})
        
        if request.user == listing.seller:
             return JsonResponse({"success": False, "message": "You cannot bid on your own item!"})

        # Save the new bid and update listing price
        new_bid = Bid(amount=bid_amount, user=request.user, listing=listing)
        new_bid.save()
        
        listing.current_price = bid_amount
        listing.save()

        return JsonResponse({"success": True, "new_price": bid_amount})