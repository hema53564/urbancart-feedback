from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "email", "rating", "status", "created_at")
    list_filter = ("status", "rating", "created_at")
    search_fields = ("customer_name", "email", "comment")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Customer Identity", {"fields": ("customer_name", "email")}),
        ("Content & Score", {"fields": ("rating", "comment", "status")}),
        ("System Information", {"fields": ("created_at", "updated_at")}),
    )