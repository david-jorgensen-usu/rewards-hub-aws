from django.urls import path
from . import views

urlpatterns = [
    path("feedback/", views.feedback_api, name="feedback_api"),
    path("user/", views.current_user, name="current_user"),
    path("user/programs/", views.programs, name="programs"),
    path("link-app/", views.link_app, name="link_app"),
    path("unlink-app/", views.unlink_app, name="unlink_app"),
    path("delete-account/", views.delete_account_api, name="delete-account"),
    path("save-notification/", views.save_notification, name="save-notification"),
]