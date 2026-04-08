from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm , UserregistrationForm
from django.contrib.auth.decorators import login_required  #use for protected route
from django.contrib.auth import login
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    query = request.GET.get('q')  # search term from navbar
    if query:
        # Filter tweets where user__username matches query (case-insensitive)
        tweets = Tweet.objects.filter(
            user__username__icontains=query
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.all().order_by('-created_at')
    
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required #create decorater so only login user an create tweet
def tweet_create(request):
    if request.method=='POST':
       form = TweetForm(request.POST ,request.FILES)
       if form.is_valid():# only login user can create post
         tweet = form.save(commit=False)
         tweet.user = request.user
         tweet.save()
         return redirect('tweet_list')
    else:
       form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})

@login_required
def tweet_edit(request , tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id, user=request.user)
    if request.method=='POST':
       form = TweetForm(request.POST ,request.FILES,instance=tweet)
       if form.is_valid():# only login user can create post
         tweet = form.save(commit=False)
         tweet.user = request.user
         tweet.save()
         return redirect('tweet_list')
    else:
     form =  TweetForm(instance=tweet)
     return render(request, 'tweet_form.html', {'form':form})

@login_required
def tweet_delete(request , tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=='POST':
         tweet.delete()
         return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})

def register(request):
    if request.method == 'POST':
        form = UserregistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
        else:
            messages.error(request, "Form is invalid. Check details.")

    else:
        form = UserregistrationForm()

    return render(request, 'registration/register.html', {'form': form})
   
   