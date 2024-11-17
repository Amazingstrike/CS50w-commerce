from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)  #(Friday, November 24, 2024 - 3:24 PM)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class User(AbstractUser):
    pass

class Products(BaseModel):
    categories = [
        ("Electronics", "Electronics"),
        ("Clothing", "Clothing"),
        ("Home", "Home"),
        ("Toys", "Toys"),
        ("Sports", "Sports"),
        ("Other", "Other"),
        ("Art", "Art"),
        ("Baby", "Baby"),
        ("Beauty", "Beauty"),
        ("Books", "Books"),
        ("Business", "Business"),
        ("Camera", "Camera"),
        ("Cell Phones", "Cell Phones"),
        ("Coins", "Coins"),
        ("Collectibles", "Collectibles"),
        ("Computers", "Computers"),
        ("Crafts", "Crafts"),
        ("Health", "Health"),
        ("Home Garden", "Home Garden"),
        ("Jewelry", "Jewelry"),
        ("Musical Instruments", "Musical Instruments"),
        ("Pet Supplies", "Pet Supplies"),
        ("Real Estate", "Real Estate"),
        ("Specialty Services", "Specialty Services"),
        ("Sporting Goods", "Sporting Goods"),
        ("Tickets", "Tickets"),
        ("Toys Hobbies", "Toys Hobbies"),
        ("Travel", "Travel"),
        ("Video Games", "Video Games"),
        ("Others", "Others"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bid_count = models.IntegerField(blank=True, null=True, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", default=1)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products_won", blank=True, null=True)
    img = models.ImageField(blank=True, null= True, default='unknown.png', upload_to="product_images/")
    category = models.CharField(max_length=64, choices=categories, blank=True, null=True)

    def __str__(self):
        return self.title

class Bids(BaseModel):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_made")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_win = models.BooleanField(default=False)

class Comments(BaseModel):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="comments")
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented")
    text = models.TextField(max_length=1000)


class Watchlist(BaseModel):
    id = models.AutoField(primary_key=True) 
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_watchlists")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Watchlist")
