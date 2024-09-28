from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView, PasswordResetDoneView
from .models import UserProfile, WorkImage
from .forms import UserProfileForm, WorkImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import CustomUserCreationForm

# Home view
def home_view(request):
    if request.user.is_authenticated:
        work_images = WorkImage.objects.filter(user=request.user)
    else:
        work_images = []  # Empty list or default images for anonymous users

    return render(request, 'home.html', {'work_images': work_images})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required(login_url='login')
def submit_image_view(request):
    if request.method == 'POST':
        form = WorkImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('work_gallery')  # Redirect to work_gallery after successful submission
    else:
        form = WorkImageForm()

    # Pass uploaded images for display
    images = WorkImage.objects.filter(user=request.user)
    return render(request, 'submit_image.html', {'form': form, 'work_images': images})


@login_required(login_url='login')
def work_gallery_view(request):
    work_images = WorkImage.objects.filter(user=request.user)
    return render(request, 'work_gallery.html', {'work_images': work_images})



@login_required(login_url='login')
def profile_view(request):
    # Ensure a UserProfile exists for the user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'profile.html', {'profile': profile})


@login_required(login_url='login')
def profile_edit_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Handle both User and UserProfile updates
        user_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid():
            # Update User model fields (username, email)
            user.username = user_form.cleaned_data['username']
            user.email = user_form.cleaned_data['email']
            user.save()  # Save changes to User model

            # Save changes to UserProfile model
            user_form.save()
            return redirect('profile')
    else:
        # Prepopulate form with both User and UserProfile data
        initial_data = {'username': user.username, 'email': user.email}
        user_form = UserProfileForm(instance=profile, initial=initial_data)

    return render(request, 'profile_edit.html', {
        'form': user_form,
    })


# Information view
def information_view(request):
    return render(request, 'information.html')

