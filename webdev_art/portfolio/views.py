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
    work_images = WorkImage.objects.filter(user=request.user)
    return render(request, 'home.html', {'work_images': work_images})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # ดูข้อผิดพลาดที่เกิดขึ้น
    else:
        form = UserCreationForm()

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
    user = request.user  # ข้อมูลของผู้ใช้งานปัจจุบัน
    try:
        profile = user.userprofile  # ตรวจสอบว่าผู้ใช้มีโปรไฟล์หรือไม่
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # อัปเดตข้อมูลโปรไฟล์
        user_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=profile)

    # แสดงฟอร์มพร้อมกับข้อมูลของผู้ใช้
    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'user': user,  # ข้อมูลผู้ใช้ เช่น username, email
    })

# Information view
def information_view(request):
    return render(request, 'information.html')