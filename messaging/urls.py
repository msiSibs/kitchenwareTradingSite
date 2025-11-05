from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation'),
    path('send/', views.send_message_view, name='send'),
]
