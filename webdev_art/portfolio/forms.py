# accounts/forms.py
from .models import UserProfile, WorkImage
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_picture','username', 'email', 'quote', 'facebook_url', 'X_url', 'instagram_url',]

# Form for WorkImage
class WorkImageForm(forms.ModelForm):
    class Meta:
        model = WorkImage
        fields = ['image', 'title', 'description']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add the email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Include the email in the fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Set the email
        if commit:
            user.save()
        return user