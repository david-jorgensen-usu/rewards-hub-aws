from django.contrib import admin
from .models import (
    AppCategory,
    AppCatalog,
    LinkedApp,
    Notification,
    UserPreference,
    AuditLog,
)

@admin.register(AppCategory)
class AppCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(AppCatalog)
class AppCatalogAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(LinkedApp)
class LinkedAppAdmin(admin.ModelAdmin):
    list_display = ("user", "app", "username")
    search_fields = ("user__username", "app__name", "username")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "read", "created_at")
    search_fields = ("title", "message")
    list_filter = ("read", "created_at")


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "dark_mode", "notifications_enabled")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "created_at")
    search_fields = ("action", "details")
    list_filter = ("created_at",)
