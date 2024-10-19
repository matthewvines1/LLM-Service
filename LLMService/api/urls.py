from django.urls import path
from . import views

urlpatterns = [
    path('llm-request/', views.llm_request, name='llm_request'),
    path('view_chats/', views.view_chats, name='view_chats'),
]