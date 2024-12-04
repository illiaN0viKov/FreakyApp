from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import EventForm, TopicForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Event, Profile
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from datetime import datetime, date

from .models import Event, Topic
from datetime import datetime

from datetime import date

 


#for home page
def home(request):
     return render(request, 'home/home.html')

#for event page
def events(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topic_filter = request.GET.get('topic', None)  

   
    query_filter = Q(title__icontains=q) | Q(description__icontains=q)

   
    if topic_filter:
        query_filter &= Q(topics__name=topic_filter)

    events = Event.objects.filter(query_filter)

    topics = Topic.objects.all()
        
    field_titles = {
        'host': Event._meta.get_field('host').verbose_name,
        'title': Event._meta.get_field('title').verbose_name,
        'description': Event._meta.get_field('description').verbose_name,
        'date': Event._meta.get_field('date').verbose_name,
        'maxPeople': Event._meta.get_field('maxPeople').verbose_name,
        'topics': Event._meta.get_field('topics').verbose_name,
    }
    context = {'events': events, 'field_titles': field_titles}
    return render(request, 'home/event_page.html', context)


##################################################################################
#creating event page
@login_required(login_url='login')
def create_event(request):
    if request.method == 'POST':
        eventForm=EventForm(request.POST, request.FILES)
        topicForm=TopicForm(request.POST)
        
        if eventForm.is_valid() and topicForm.is_valid():
           
            event = eventForm.save(commit=False)  # Create the Event instance without saving to the database
            event.host = request.user  # Add the host manually
            event.save() 
            # Save the selected topics
            topics = topicForm.cleaned_data['topics']
            event.topics.set(topics)

            messages.success(request, f"Event '{event.title}' created successfully!")
            return redirect('event-created')  # Redirect to a relevant page
    else:
        eventForm = EventForm()
        topicForm = TopicForm()

    context={'eventForm': eventForm,
             'topicForm':topicForm}
    return render(request, 'home/create_event.html', context)

'''
@login_required(login_url='login')
def create_event_preview(request):
    event_data = request.session.get('event_data')
    if not event_data:
        return redirect('create-event')
    
    event_data['date'] = datetime.fromisoformat(event_data['date'])
    topics = Topic.objects.filter(id__in=event_data.get('topics', []))
    event_data['host'] = request.user.username

    if request.method == "POST":

        event = Event.objects.create(
            host=request.user,
            title=event_data['title'],
            description=event_data['description'],
            date=event_data['date'],
            maxPeople=event_data['maxPeople'],
            picture=request.FILES.get('picture') 
        )

        event.topics.set(topics)
        request.session.pop('event_data', None)
        messages.success(request, f"Event '{event.title}' created successfully!")
        return redirect('event-created')
    
    return render(request, "home/create_event_preview.html", {"event_data":event_data, "topics":topics, })

'''
def event_created(request):
    if not messages.get_messages(request):
        return redirect('home')
    return render(request, 'home/event_success_page.html')

  
##################################################################################


@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    return render(request, 'home/profile.html', {'profile': profile})




def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)


    return render(request, 'home/edit_profile.html', {'form': form})



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
    today = date.today()  # Get today's date (not including time)

    # Delete events with a date before today
    Event.objects.filter(date__lt=today).delete()

    # Fetch non-expired events for the current user
    myevents = Event.objects.filter(host=request.user, date__gte=today)

    field_titles = {
        'host': Event._meta.get_field('host').verbose_name,
        'title': Event._meta.get_field('title').verbose_name,
        'picture': Event._meta.get_field('picture').verbose_name,
        'description': Event._meta.get_field('description').verbose_name,
        'date': Event._meta.get_field('date').verbose_name,
        'maxPeople': Event._meta.get_field('maxPeople').verbose_name,
        'topics': Event._meta.get_field('topics').verbose_name,
    }

    context = {
        'myevents': myevents,
        'field_titles': field_titles,
    }
    return render(request, 'home/my_events.html', context)






@login_required(login_url='login')
def editEvent(request, pk):
    try:
        event = Event.objects.get(id=pk)
    except Event.DoesNotExist:
        return HttpResponse('Event not found.')

    if request.user != event.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        eventForm = EventForm(request.POST, request.FILES, instance=event)
        topicForm = TopicForm(request.POST)

        if eventForm.is_valid() and topicForm.is_valid():
            event = eventForm.save(commit=False)  # Save Event data
            event.host = request.user  # Ensure the host is the current user (just in case)
            event.save()

            # Save the selected topics
            topics = topicForm.cleaned_data['topics']
            event.topics.set(topics)

            messages.success(request, f"Event '{event.title}' updated successfully!")
            return redirect('event-details', pk=event.pk)  # Redirect to the event detail page (or another relevant page)
    else:
        eventForm = EventForm(instance=event)
        topicForm = TopicForm(initial={'topics': event.topics.all()})  # Prepopulate the form with selected topics

    context = {'eventForm': eventForm, 'topicForm': topicForm, 'event': event}
    return render(request, 'home/edit_event.html', context)


'''
def editPreview(request):
    event_data = request.session.get('saved_event_data')
    if not event_data:
        return redirect('edit-event')

    try:
        event = Event.objects.get(id=event_data.get('id'))
    except Event.DoesNotExist:
        return HttpResponse("Event does not exist.")

    topics = Topic.objects.filter(id__in=event_data.get('topics', []))

    if request.method == "POST":
        event.title = event_data['title']
        event.description = event_data['description']
        event.date = event_data['date']
        event.maxPeople = event_data['maxPeople']
        event.save()

        if topics:
            event.topics.set(topics)

        messages.success(request, f"Event '{event.title}' updated successfully!")
        request.session.pop('saved_event_data', None)  # Clear session data
        return redirect('edited-event')

    return render(request, 'home/edit_event_preview.html', {'event_data': event_data, 'topics': topics})
'''


def deleteEvent(request, pk):
    event=Event.objects.get(id=pk)

#checking if the user who want to delete a room is the same who create it
    if request.user != event.host:
        return HttpResponse('You are not allowed here!!')

    if request.method=='POST':
        event.delete()
        return redirect('home')
    return render(request, 'home/delete_event.html', {'obj':event})


def event_details(request, pk):
    event= get_object_or_404(Event, pk=pk)
    user_has_joined = event.is_user_joined(request.user)
    has_space = event.has_space()
    return render(request, 'home/event_details.html', {'event': event, 'user_has_joined': user_has_joined,
                                                        'has_space': has_space})



@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.participants.add(request.user)
    return redirect('event-details', pk=pk)


def calendar_view(request):
    if request.user.is_authenticated:
        joined_events = Event.objects.filter(participants=request.user)
        events = [
            {
                "title": event.title,
                "start": event.date.isoformat(),
                "url": reverse('event-details', args=[event.id])  # generates the event details URL
            }
            for event in joined_events
        ]
    else:
        events = []  # empty list for anonymous users

    return render(request, 'home/calendar.html', {'events': events})
