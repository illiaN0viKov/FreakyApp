from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage
from .forms import *


@login_required
def chat_view(request, chat_name): 
    chat_group = get_object_or_404(ChatGroup, chat_name = chat_name)
    if request.user != chat_group.event.host and not chat_group.event.is_user_joined(request.user):
        return HttpResponseForbidden("You do not have permission to access this chat.")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = MessageForm()
    
    if request.headers.get('HX-Request'):
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                "message": message,
                "user": request.user,
            }

            return render(request, 'chat/partials/chat_message_p.html', context)

    return render(request, 'chat/chat.html', {"chat_messages":chat_messages, "form": form,  "chat_name":chat_group.chat_name})


