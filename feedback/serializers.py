from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    """
    Validates and formats incoming API feedback request data.
    """
    class Meta:
        model = Feedback
        fields = [
            "id",
            "customer_name",
            "email",
            "rating",
            "comment",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_customer_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Customer name cannot be blank.")
        return value

    def validate_comment(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Comment cannot be blank.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be an integer between 1 and 5.")
        return value