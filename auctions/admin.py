from django.contrib import admin
from .models import User, Products, Bids, Comments, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Products)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)
