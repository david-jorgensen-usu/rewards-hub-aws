from django.db import models
from django.contrib.auth.models import User


class AppCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AppCatalog(models.Model):
    name = models.CharField(max_length=200, unique=True)
    reference = models.CharField(max_length=200)
    category = models.ForeignKey(AppCategory, on_delete=models.CASCADE, related_name="apps")

    def __str__(self):
        return self.name


class LinkedApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="linked_apps")
    app = models.ForeignKey(AppCatalog, on_delete=models.CASCADE, related_name="linked_users")
    notify = models.BooleanField(default=True)  # short, conveys notifications status

    def __str__(self):
        status = "🔔" if self.notify else "🔕"
        return f"{self.user.username} → {self.app.name} {status}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Read" if self.read else "Unread"
        return f"{self.title} ({status})"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user or 'Anonymous'} at {self.created_at:%Y-%m-%d}"
