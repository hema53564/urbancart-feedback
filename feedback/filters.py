import django_filters
from .models import Feedback

class FeedbackFilter(django_filters.FilterSet):
    """
    Filter set to handle rating and status configurations cleanly.
    """
    rating = django_filters.NumberFilter(field_name="rating")
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=Feedback.Status.choices
    )

    class Meta:
        model = Feedback
        fields = ["rating", "status"]