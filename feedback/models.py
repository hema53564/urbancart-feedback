from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Feedback(models.Model):
    """
    Stores customer feedback submitted by support staff or customers.
    """
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        REVIEWED = "Reviewed", "Reviewed"

    customer_name = models.CharField(
        max_length=100,
        help_text="Customer's full name."
    )
    email = models.EmailField(
        help_text="Customer's contact email address."
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating score out of 5."
    )
    comment = models.TextField(
        max_length=1000,
        help_text="Customer comments."
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Current review lifecycle state."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["rating"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.customer_name} ({self.rating}/5 - {self.status})"
# Create your models here.
