from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import EventForm, TopicForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Event, Topic
from datetime import datetime
 

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


##################################################################################
#creating event page
@login_required(login_url='login')
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event_data = form.cleaned_data
            event_data['date'] = event_data['date'].isoformat()  # Convert datetime to string
            request.session['event_data'] = event_data
            return redirect('create-event-topic')
    else:
        form = EventForm()
    return render(request, 'home/create_event.html', {'form': form})

@login_required(login_url='login')
def create_event_topic(request):
    if 'event_data' not in request.session:
        return redirect('create-event') 

    event_data = request.session.get('event_data')
    # event_data['date'] = datetime.fromisoformat(event_data['date'])

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            event_data['topics'] = list(form.cleaned_data['topics'].values_list('id', flat=True))
            request.session['event_data'] = event_data 
            return redirect('create-event-preview')  # Redirect to preview page
    else:
        form = TopicForm()

    return render(request, 'home/create_event_topic.html', {'form': form, 'event_data': event_data})


#(work here)
@login_required(login_url='login')
def create_event_preview(request):
    event_data = request.session.get('event_data')
    if not event_data:
        return redirect('create-event')
    
    event_data['date'] = datetime.fromisoformat(event_data['date'])
    topics = Topic.objects.filter(id__in=event_data.get('topics', []))

    if request.method == "POST":

        event = Event.objects.create(
            host=request.user,
            title=event_data['title'],
            description=event_data['description'],
            date=event_data['date'],
            maxPeople=event_data['maxPeople'],
        )
        event.topics.set(topics)
        request.session.pop('event_data', None)
        messages.success(request, f"Event '{event.title}' created successfully!")
        return redirect('event-created')
    
    return render(request, "home/create_event_preview.html", {"event_data":event_data, "topics":topics})


def event_created(request):
    if not messages.get_messages(request):
        return redirect('home')
    return render(request, 'home/event_success_page.html')


##################################################################################


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

def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        

def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page after saving
            return redirect('login')  # Adjust 'login' to match your URL name for the login page
    else:
        form = UserCreationForm()  # Initialize an empty form for GET requests

    return render(request, 'home/regist.html', {'form': form})


#open only when you already logIn
def myEvents(request):
    myevents = Event.objects.filter(host=request.user)
    field_titles = {
        'host': Event._meta.get_field('host').verbose_name,
        'title': Event._meta.get_field('title').verbose_name,
        'description': Event._meta.get_field('description').verbose_name,
        'date': Event._meta.get_field('date').verbose_name,
        'maxPeople': Event._meta.get_field('maxPeople').verbose_name,
    }
    context={'myevents':myevents,
             'field_titles':field_titles}
    return render(request, 'home/my_events.html', context)

