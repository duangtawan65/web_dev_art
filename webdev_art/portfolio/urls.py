# In your `urls.py`
from django.urls import path
from .views import home_view, register_view, submit_image_view, work_gallery_view, information_view, profile_view, profile_edit_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [

    path('', home_view, name='home'),
    # authentication
    path('', lambda request: redirect('login')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),


# Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Password change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),


    #proflie
    path('profile/', profile_view, name='profile'),
    path('submit_image/', submit_image_view, name='submit_image'),
    path('work_gallery/', work_gallery_view, name='work_gallery'),
    path('information/', information_view, name='information'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

