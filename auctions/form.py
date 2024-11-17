from django.forms import ModelForm
from .models import Products, Comments, Bids


class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ['title', 'starting_bid', 'description', 'category', 'img']
        labels = {'img' : 'Image'}

class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ["amount"]
        labels = {'amount' : ''}

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["text"]
        labels = {"text" : ""}
