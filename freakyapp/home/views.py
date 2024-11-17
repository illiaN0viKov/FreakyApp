from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import EventForm

#for home page
def home(request):
     return render(request, 'home/home.html')

#for event page
def event(request):
     return render(request, 'home/event_page.html')


#creating event page
@login_required(login_url='login')
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            # Save the form and associate the logged-in user as the host
            event = form.save(commit=False) 
            event.host = request.user  
            event.save()  
            return redirect('home')
    else:
        form = EventForm()

    return render(request, 'home/create_event.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    return render(request, 'home/profile.html', {'profile': profile})



class CustomLogInView(LoginView):
     template_name = "home/logi_reg.html"
     redirect_authenticated_user = True

class CustomLogOutView(LogoutView):
    def get_next_page(self):
        return reverse('success-logout')  # Redirect to the success-logout URL

def success_logout(request):
    # If the user is still authenticated, redirect them away
    if request.user.is_authenticated:
        return redirect('home')  # Or any page you prefer
    return render(request, 'home/log_out.html')

