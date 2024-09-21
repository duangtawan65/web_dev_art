from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from .models import UserProfile, WorkImage
from .forms import UserProfileForm, WorkImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile

# Home view
def home_view(request):
   return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html',{'form':form})

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def submit_image_view(request):
    if request.method == 'POST':
        form = WorkImageForm(request.POST, request.FILES)
        if form.is_valid():
            work_image = form.save(commit=False)
            work_image.user = request.user  # Associate image with the user
            work_image.save()
            return redirect('home')
    else:
        form = WorkImageForm()
    return render(request, 'submit_image.html', {'form': form})


@login_required
def profile_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})

# Work image gallery view
def work_gallery_view(request):
    work_images = WorkImage.objects.all()  # Assuming you're displaying all images
    return render(request, 'work_gallery.html', {'work_images': work_images})

# Information view
def information_view(request):
    return render(request, 'information.html')