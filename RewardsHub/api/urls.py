from django.urls import path
from . import views

urlpatterns = [
    path("test-api/", views.test_api, name="test_api"),
    path("feedback/", views.feedback_api, name="feedback_api"),
    path("user/", views.current_user, name="current_user"),
]