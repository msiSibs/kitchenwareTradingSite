from django.shortcuts import render
from django.http import HttpResponse

# Stub views for messaging app - to be implemented in Phase 5

def inbox_view(request):
    return HttpResponse("Inbox View - Coming in Phase 5")

def conversation_view(request, user_id):
    return HttpResponse("Conversation View - Coming in Phase 5")

def send_message_view(request):
    return HttpResponse("Send Message View - Coming in Phase 5")
