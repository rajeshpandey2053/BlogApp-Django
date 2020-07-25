from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
                                ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView
                                )
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required(login_url='home:login')
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'home/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    def get_success_url(self):
        return (reverse('home:home'))
    

def about(request):
    return render(request, 'home/about.html', {'title': 'About'})