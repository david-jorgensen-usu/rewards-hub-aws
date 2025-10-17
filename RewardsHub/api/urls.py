from django.urls import path
from . import views, current_user

urlpatterns = [
    path("test-api/", views.test_api, name="test_api"),
    path("feedback/", views.feedback_api, name="feedback_api"),
    path("user/", current_user, name="current_user"),
]