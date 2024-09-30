from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView, PasswordResetDoneView
from .models import UserProfile, WorkImage
from .forms import UserProfileForm, WorkImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile,Follow
from .forms import CustomUserCreationForm
from django.http import JsonResponse

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
        # Check if the form is for deleting an image
        if 'delete_image' in request.POST:
            image_id = request.POST.get('delete_image')
            image = get_object_or_404(WorkImage, id=image_id, user=request.user)  # Ensure that only the user's own images are deleted
            image.delete()  # Delete the image
            return redirect('submit_image')  # Redirect to the same page after deletion

        # Handle image submission form
        form = WorkImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user  # Attach the current user to the image
            image.save()
            return redirect('work_gallery')  # Redirect to the gallery after successful submission
    else:
        form = WorkImageForm()

    # Fetch the images uploaded by the current user
    images = WorkImage.objects.filter(user=request.user)
    return render(request, 'submit_image.html', {'form': form, 'work_images': images})


@login_required(login_url='login')
def work_gallery_view(request, username=None):
    # If a username is provided, show that user's gallery
    user = get_object_or_404(User, username=username)
    work_images = WorkImage.objects.filter(user=user)
    return render(request, 'work_gallery.html', {'work_images': work_images, 'viewed_user': user})



@login_required(login_url='login')
def profile_view(request, username=None):
    # ถ้ามี username ให้แสดงโปรไฟล์ของผู้ใช้นั้น
    # ถ้าไม่มี ให้แสดงโปรไฟล์ของผู้ใช้ที่ล็อกอินอยู่
    if username:
        viewed_user = get_object_or_404(User, username=username)
    else:
        viewed_user = request.user

    # ตรวจสอบว่าผู้ใช้ที่ดูโปรไฟล์ติดตามผู้ใช้นี้อยู่หรือไม่
    is_following = Follow.objects.filter(follower=request.user, following=viewed_user).exists()

    # สร้างหรือดึง UserProfile ของผู้ใช้นั้น
    profile, created = UserProfile.objects.get_or_create(user=viewed_user)

    # นับจำนวน followers และ following
    followers_count = Follow.objects.filter(following=viewed_user).count()
    following_count = Follow.objects.filter(follower=viewed_user).count()

    return render(request, 'profile.html', {
        'profile': profile,
        'viewed_user': viewed_user,
        'is_following': is_following,  # ส่งสถานะการติดตามไปที่ template
        'followers_count': followers_count,  # ส่งจำนวน followers ไปที่ template
        'following_count': following_count  # ส่งจำนวน following ไปที่ template
    })




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
            return redirect('profile', username=user.username)  # เปลี่ยนเป็นหน้าโปรไฟล์หลังแก้ไข
    else:
        # Prepopulate form with both User and UserProfile data
        initial_data = {'username': user.username, 'email': user.email}
        user_form = UserProfileForm(instance=profile, initial=initial_data)

    return render(request, 'profile_edit.html', {
        'form': user_form,
    })

def search_work_gallery_view(request):
    search_query = request.GET.get('search')
    if search_query:
        try:
            user = User.objects.get(username=search_query)
            return redirect('work_gallery', username=user.username)  # Redirect to the user's gallery
        except User.DoesNotExist:
            return render(request, 'home.html', {'error': 'User not found'})  # Handle user not found
    else:
        return redirect('home')  # If no search query, redirect back to the homepage



@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=user_to_follow.username)

# ฟังก์ชันสำหรับเลิกติดตามผู้ใช้
@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=user_to_unfollow.username)




def username_autocomplete(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=query)[:10]
        results = []
        for user in users:
            results.append({'label': user.username})
        return JsonResponse(results, safe=False)
