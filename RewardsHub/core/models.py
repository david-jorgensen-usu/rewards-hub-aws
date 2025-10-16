from django.db import models
from django.contrib.auth.models import User

class AppCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)


class AppCatalog(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="app_logos/")
    category = models.ForeignKey(AppCategory, on_delete=models.CASCADE, related_name="apps")


class LinkedApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="linked_apps")
    app = models.ForeignKey(AppCatalog, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # encrypt later


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    dark_mode = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
