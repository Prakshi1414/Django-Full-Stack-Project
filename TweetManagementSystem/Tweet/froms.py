from django import froms
from .models import Tweet

class TweetForm(froms.ModelForm):
    class meta:
        model = Tweet
        fields = ['text', 'photo']
