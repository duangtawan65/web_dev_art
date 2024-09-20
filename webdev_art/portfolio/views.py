from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
