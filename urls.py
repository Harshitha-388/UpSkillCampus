from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("create/", views.create_listing, name="create"),
    path("listing/<int:id>", views.listing_detail, name="listing_detail"),
    path("listing/<int:id>/bid", views.add_bid, name="add_bid"),
    
]

admin.site.site_header = "Online Auction Portal"
admin.site.site_title = "Auction Admin"
admin.site.index_title = "Welcome to the Auction Management System"