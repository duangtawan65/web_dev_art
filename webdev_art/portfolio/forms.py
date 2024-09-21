# accounts/forms.py
from django import forms
from .models import UserProfile, WorkImage

# Form for UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['quote', 'facebook_url', 'X_url', 'instagram_url']

# Form for WorkImage
class WorkImageForm(forms.ModelForm):
    class Meta:
        model = WorkImage
        fields = ['image', 'title', 'description']
