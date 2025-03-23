# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    mobile_number = forms.CharField(max_length=15, required=False, help_text='Required. Enter a valid mobile number.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile_number', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    username = forms.CharField(max_length=150, required=True)
    mobile_number = forms.CharField(max_length=15, required=False, help_text='Required. Enter a valid mobile number.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile_number')
                
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if username is being changed
        if username != self.instance.username:
            # Check if new username already exists
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with that username already exists.')
        return username

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Current Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm New Password")
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Your current password is incorrect.')
        return old_password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('The two password fields didn\'t match.')
        return cleaned_data
    
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class UsernamePasswordResetForm(forms.Form):
    """
    Form for requesting a password reset using username instead of email
    """
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter your username and we'll send an email to the address associated with your account."
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        
        if not user:
            raise forms.ValidationError("We couldn't find an account with that username.")
        
        if not user.email:
            raise forms.ValidationError("This account doesn't have an email address.")
        
        # Store the user object for later use in the view
        self.user_cache = user
        return username

class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom form for setting a new password
    """
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )