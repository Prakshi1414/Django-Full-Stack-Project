from django.shortcuts import render
from .models import Tweet
from .froms import TweetForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

#list vall tweets in one page
def tweet_list(request):
   tweets= Tweet.objects.all().order_by('-created_at')
   return render(request, 'tweet_list.html', {'tweets':tweets})

def tweet_create(request):
    if request.method=='post':
       form = TweetForm(request.Post ,request.FILES)
       if form.is_valid():# only login user can create post
         tweet = form.save(commite=False)
         tweet.user = request.user
         tweet.save()
         return redirect('tweet_list')
    else:
       form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form})

def tweet_edit(request , tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id, user=request.user)
    if request.method=='post':
       form = TweetForm(request.Post ,request.FILES, isinstance=tweet)
       if form.is_valid():# only login user can create post
         tweet = form.save(commite=False)
         tweet.user = request.user
         tweet.save()
         return redirect('tweet_list')
    else:
     form =  TweetForm(isinstance=tweet)
     return render(request, 'tweet_form.html', {'form':form})


def tweet_delete(request , tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=='post':
         tweet.delete()
         return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})
   