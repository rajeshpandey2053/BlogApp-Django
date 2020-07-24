from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required(login_url='home:login')
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})