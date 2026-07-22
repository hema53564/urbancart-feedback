import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import FeedbackFilter
from .models import Feedback
from .serializers import FeedbackSerializer
from .utils import export_feedback_to_csv

logger = logging.getLogger(__name__)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    Handles API endpoints for creating, listing, and transitioning feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    
    # FIXED: The bracketed backend list prevents the syntax crash
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackFilter
    
    # Explicitly allow safe HTTP operations
    http_method_names = ["get", "post", "patch", "head", "options"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
        except Exception:
            logger.exception("Database write failure encountered during feedback submission.")
            return Response(
                {"message": "An unexpected error occurred while saving feedback. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Operational support logging with rich contextual metadata, avoiding PII exposure
        logger.info(
            "New feedback registered successfully.",
            extra={
                "rating": serializer.validated_data["rating"],
            }
        )
        return Response(
            {
                "message": "Feedback submitted successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        """
        Explicitly block delete operations to ensure transaction history is immutable.
        """
        logger.warning("Feedback deletion request rejected.")
        return Response(
            {"detail": "Deleting feedback is not allowed in this system."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, methods=["patch"])
    def review(self, request, pk=None):
        """
        Custom business endpoint to transition feedback state to Reviewed.
        Implements an idempotent pattern for workflow stability.
        """
        feedback = self.get_object()

        if feedback.status == Feedback.Status.REVIEWED:
            return Response(
                {"message": "Feedback is already marked as Reviewed."},
                status=status.HTTP_200_OK
            )

        feedback.status = Feedback.Status.REVIEWED
        feedback.save()

        logger.info(
            "Feedback status successfully updated.",
            extra={
                "feedback_id": feedback.id,
                "transition_to": "Reviewed"
            }
        )
        return Response(
            {"message": "Feedback marked as Reviewed."},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def export(self, request):
        """
        Triggers CSV file generation for filtered or raw queryset items.
        """
        queryset = self.filter_queryset(self.get_queryset())
        logger.info(
            "Feedback CSV export triggered.",
            extra={"records_exported": queryset.count()}
        )
        return export_feedback_to_csv(queryset)
