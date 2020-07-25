 
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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


# @method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'users/profile.html'
    success_url = '/home/home/'
        
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
                 

    