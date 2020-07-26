 
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# start here for email registrations
import json
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.views import View
from django.contrib.auth.views import LoginView


from .tokens import user_tokenizer

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html', { 'form': UserRegisterForm() })

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            url = 'http://localhost:8000' + reverse('home:confirm_email', kwargs={'user_id': user_id, 'token': token})
            message = get_template('users/register_email.html').render({
              'confirm_url': url
            })
            mail = EmailMessage('Django users Email Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()

            return render(request, 'users/login.html', {
              'form': AuthenticationForm(),
              'message': f'A confirmation email has been sent to {user.email}. Please confirm to finish registering'
            })

        return render(request, 'users/register.html', { 'form': form })

class ConfirmRegistrationView(LoginView):

    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        
        user = User.objects.get(pk=user_id)

        context = {
          'form': AuthenticationForm()
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_valid = True
            user.save()
            

        return render(request, 'users/login.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Profile.objects.filter(pk = ram):
            new_context_entry = 0
        else:          
            new_context_entry = 1
        context["create"] = new_context_entry
        return context

            



    # END HERE email registration


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('home:login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})




# @login_required(login_url='home:login')
# def profile(request):
#     if request.method == 'POST':
#         if Profile.objects.filter(user=request.user):
#             u_form = UserUpdateForm(request.POST, instance=request.user)
#             p_form = ProfileUpdateForm(request.POST, 
#                                     request.FILES, instance=request.user.profile)
#         else:
#             u_form = UserUpdateForm(request.POST,instance=request.user)
#             p_form = ProfileUpdateForm(request.POST, 
#                                     request.FILES)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated')
#             return redirect('home:profile')

#     else: 
#         if Profile.objects.filter(user=request.user):
                
#             u_form = UserUpdateForm( instance=request.user)
#             p_form = ProfileUpdateForm(instance = request.user.profile)  
#             context = {
#             'u_form': u_form,
#             'p_form': p_form
#             }
#             return render(request, 'users/profile.html', context)
#         else: 
#             u_form = UserUpdateForm(instance=request.user)
#             p_form = ProfileUpdateForm()  
#             context = {
#             'u_form': u_form,
#             'p_form': p_form
#             }
#             return render(request, 'users/profile.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileCreateView(CreateView):
    form_class = ProfileForm
    template_name = 'users/createprofile.html'
    context_object_name = 'user'
    success_url = '/home/home/'

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Profile.objects.filter(user=self.request.user):
            new_context_entry = 0
        else:          
                                
            new_context_entry = 1
        context["create"] = new_context_entry
        return context



    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'users/profile.html'
    success_url = '/home/home/'
        
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
                 

    