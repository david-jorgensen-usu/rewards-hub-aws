from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test-api/", views.test_api, name="test_api"),
    path("feedback/", views.feedback_api, name="feedback_api"),
]