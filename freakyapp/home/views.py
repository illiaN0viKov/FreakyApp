from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Event
 

#for home page
def home(request):
     return render(request, 'home/home.html')

#for event page
def events(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    events=Event.objects.all()
    field_titles = {
        'host': Event._meta.get_field('host').verbose_name,
        'title': Event._meta.get_field('title').verbose_name,
        'description': Event._meta.get_field('description').verbose_name,
        'date': Event._meta.get_field('date').verbose_name,
        'maxPeople': Event._meta.get_field('maxPeople').verbose_name,
    }
    context = {'events': events, 'field_titles': field_titles}
    return render(request, 'home/event_page.html', context)


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
            messages.success(request, "Event created successfully!")
            return redirect('event-created')
    else:
        form = EventForm()
    return render(request, 'home/create_event.html', {'form': form})

def event_created(request):
    if not messages.get_messages(request):
        return redirect('home')
    return render(request, 'home/event_success_page.html')


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

def registration(requset):
    if requset.method == "POST":
        form = UserCreationForm(requset.POST)
        if form.is_valid():
            form.save()
        
    return render(request, 'home/regist.html', {'form':form})


