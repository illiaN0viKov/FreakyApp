from django.shortcuts import render


#for home page
def home(request):
     return render(request, 'home/home.html')

#for event page
def event(request):
     return render(request, 'home/event_page.html')