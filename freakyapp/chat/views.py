from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, chat_name = "TYPE SHIT")
    chat_messages = chat_group.chat_messages.all()[:30]
    return render(request, 'chat/chat.html', {"chat_messages":chat_messages})
