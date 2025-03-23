# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import SignUpForm, UserUpdateForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import update_session_auth_hash
from .forms import SignUpForm, UserUpdateForm, PasswordChangeForm
from .models import UserProfile


class HomeView(TemplateView):
    template_name = 'accounts/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'official_profile'):
            context['is_official'] = True
        else:
            context['is_official'] = False
        return context


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/'  # Redirect to home page on success
    
    def dispatch(self, request, *args, **kwargs):
        # If user is already authenticated, log them out first
        if request.user.is_authenticated:
            logout(request)
            # Optional: Add a message to inform the user
            messages.info(request, 'You have been logged out to create a new account.')
            # Redirect back to signup page
            return redirect('signup')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        
        # Set the mobile number in the user profile if provided
        mobile_number = form.cleaned_data.get('mobile_number')
        if mobile_number:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.mobile_number = mobile_number
            profile.save()
        
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        messages.success(self.request, f'Account created for {username}! You are now logged in.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# Modify ProfileView to just show profile info
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'official_profile'):
            # Redirect government officials to their dashboard
            return redirect('authorities:authority_dashboard')
        else:
            # Normal users see their profile with complaint options
            return render(request, 'accounts/profile.html', {'user': request.user})

    def form_valid(self, form):
        """Override form_valid to handle the remember me checkbox"""
        # Call the parent class's form_valid method which will set the cookie
        response = super().form_valid(form)
        
        # Check if the remember me checkbox is checked
        if self.request.POST.get('remember_me', None) != 'on':
            # If remember me is not checked, set session to expire when browser closes
            self.request.session.set_expiry(0)
        else:
            # If remember me is checked, use the longer session
            # The session length is determined by SESSION_COOKIE_AGE in settings.py
            self.request.session.set_expiry(None)
            
        return response

# Add a new view for profile editing
@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        form = UserUpdateForm(instance=request.user)
        
        # Get or create profile for the user
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Set initial mobile number from profile if it exists
        form.initial['mobile_number'] = profile.mobile_number
        
        password_form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/edit_profile.html', {
            'form': form,
            'password_form': password_form
        })
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        
        if action == 'update_profile':
            form = UserUpdateForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(user=request.user)
            
            if form.is_valid():
                user = form.save()
                
                # Get or create profile
                profile, created = UserProfile.objects.get_or_create(user=user)
                
                # Update the profile's mobile number
                profile.mobile_number = form.cleaned_data.get('mobile_number', '')
                profile.save()
                
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('profile')
                
        elif action == 'change_password':
            form = UserUpdateForm(instance=request.user)
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            
            if password_form.is_valid():
                password_form.save()
                # Update the session to prevent the user from being logged out
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('profile')
        
        return render(request, 'accounts/edit_profile.html', {
            'form': form,
            'password_form': password_form
        })


@method_decorator(login_required, name='dispatch')
class NavbarContextView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if hasattr(request.user, 'official_profile'):
            context['is_official'] = True
        else:
            context['is_official'] = False
        return context


@method_decorator(login_required, name='dispatch')
class HomeRedirectView(View):
    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'official_profile'):
            return redirect('authorities:authority_dashboard')
        return render(request, 'accounts/home.html', {'user': request.user})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        # If user is already authenticated, log them out first
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, 'You have been logged out. Please login with your credentials.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


