from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .form import ProductForm, BidForm, CommentForm
from .models import User, Products, Comments, Bids, Watchlist
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def index(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "products" : Products.objects.all(),
        "user" : user
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "GET":
        product_form = ProductForm()
        return render(request, "auctions/create.html", {
            "form" : product_form,
        })
    product_form = ProductForm(request.POST, request.FILES)
    if product_form.is_valid():
        product = product_form.save(commit=False)
        product.created_by = request.user
        product.current_bid = product.starting_bid
        product.save()
        return HttpResponseRedirect(reverse("index"))


def listing(request, id):
    if request.method == "GET":
       product = Products.objects.get(pk=id)
       bid_form = BidForm()
       comment_form = CommentForm()
       comments = Comments.objects.filter(product = id)
       if product.winner == request.user:
            return render(request, "auctions/listing.html", {
            "product" : product,
            "bid_form" : bid_form,
            "message" : "You are the winner of this Auction.",
            "comment_form" : comment_form,
            "comments" : comments,
            "watched": Watchlist.objects.filter(user=request.user, product=id).exists(),
        }) 

       return render(request, "auctions/listing.html", {
            "product" : product,
            "bid_form" : bid_form,
            "comment_form" : comment_form,
            "comments" : comments,
            "watched": Watchlist.objects.filter(user=request.user, product=id).exists(),
       }) 


@login_required
def bid(request, id):
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        comment_form = CommentForm()
        comments = Comments.objects.filter(product = id)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.user = request.user
            product = Products.objects.get(pk=id)
            bid.product = product
            if bid.amount <= product.current_bid:
                return render(request, "auctions/listing.html", {
                    "product" : product,
                    "message" : "The bid need to be greater than the current bid",
                    "bid_form" : bid_form,
                    "comment_form" : comment_form,
                    "comments" : comments,
                    "watched": Watchlist.objects.filter(user=request.user, product=id).exists()
                })
            product.current_bid = bid.amount
            product.bid_count += 1
            bid.save()
            product.save()
            return HttpResponseRedirect(reverse('listing', args=[id]))
    return HttpResponseRedirect(reverse('listing', args=[id]))


@login_required
def close(request, id):
    if request.method == "POST":
        product = Products.objects.get(pk=id)
        bid = Bids.objects.filter(product = product).order_by('-amount').first()
        if bid == None:
            product.status = False
            product.save()
            return HttpResponseRedirect(reverse("index"))
        product.winner = bid.user
        product.status = False
        product.save()
        return HttpResponseRedirect(reverse("index"))
    
    
@login_required
def comment(request, id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.commented_by = request.user
        comment.product = Products.objects.get(id=id)
        comment.save()
    return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def add_watchlist(request, id):
    product = Products.objects.get(id=id)
    Watchlist.objects.create(user=request.user, product=product)
    return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def remove_watchlist(request, id):
    Watchlist.objects.filter(user=request.user, product=id).delete()
    return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def watchlist(request):
    products = Watchlist.objects.filter(user=request.user).values_list('product', flat=True)
    return render(request, "auctions/watchlist.html", {
        "products": Products.objects.filter(id__in=products)
    })


def categories(request):
    categories = Products.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):
    return render(request, "auctions/category.html", {
        "products": Products.objects.filter(category=category),
        "category" : category
    })

