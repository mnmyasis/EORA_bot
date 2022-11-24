from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('message', views.MessageView.as_view(), name='message_view')
]
