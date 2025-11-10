from django.contrib import admin
from .models import AppCategory, AppCatalog, LinkedApp, Notification, Feedback


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
    list_display = ("user", "app", "notify")
    search_fields = ("user__username", "app__name")
    list_filter = ("notify",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "read", "created_at")
    search_fields = ("title", "message")
    list_filter = ("read", "created_at")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "short_message", "created_at")
    search_fields = ("message", "user__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def short_message(self, obj):
        return (obj.message[:50] + "...") if len(obj.message) > 50 else obj.message
    short_message.short_description = "Message"
