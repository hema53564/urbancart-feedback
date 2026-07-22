from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Feedback

class FeedbackAPITestCase(APITestCase):
    """
    Verifies functional operations across all feedback endpoints.
    """
    def setUp(self):
        self.feedback = Feedback.objects.create(
            customer_name="John Doe",
            email="john@example.com",
            rating=5,
            comment="Excellent service."
        )

    def test_create_feedback_success(self):
        url = reverse("feedback-list")
        data = {
            "customer_name": "Alice Smith",
            "email": "alice@example.com",
            "rating": 4,
            "comment": "Very good support."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Feedback submitted successfully.")
        self.assertEqual(response.data["data"]["customer_name"], "Alice Smith")
        self.assertEqual(Feedback.objects.count(), 2)

    def test_create_feedback_blank_name_fails(self):
        url = reverse("feedback-list")
        data = {
            "customer_name": "   ",
            "email": "alice@example.com",
            "rating": 4,
            "comment": "Some comment"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer_name", response.data)

    def test_create_feedback_blank_comment_fails(self):
        url = reverse("feedback-list")
        data = {
            "customer_name": "Alice Smith",
            "email": "alice@example.com",
            "rating": 4,
            "comment": ""
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("comment", response.data)

    def test_create_feedback_invalid_rating(self):
        url = reverse("feedback-list")
        data = {
            "customer_name": "Bob",
            "email": "bob@example.com",
            "rating": 6,
            "comment": "Invalid rating test."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating", response.data)

    def test_filter_by_rating(self):
        url = reverse("feedback-list")
        response = self.client.get(url, {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_status(self):
        url = reverse("feedback-list")
        response = self.client.get(url, {"status": "Pending"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_feedback_reviewed(self):
        url = reverse("feedback-review", args=[self.feedback.id])
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Feedback marked as Reviewed.")
        
        self.feedback.refresh_from_db()
        self.assertEqual(self.feedback.status, Feedback.Status.REVIEWED)

    def test_review_idempotency(self):
        """
        Verifies that marking an already-reviewed feedback as reviewed
        remains idempotent and returns a clean 200 OK.
        """
        self.feedback.status = Feedback.Status.REVIEWED
        self.feedback.save()

        url = reverse("feedback-review", args=[self.feedback.id])
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Feedback is already marked as Reviewed.")

    def test_delete_blocked(self):
        url = reverse("feedback-detail", args=[self.feedback.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_export_csv(self):
        url = reverse("feedback-export")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment", response["Content-Disposition"])

    def test_export_csv_filtered(self):
        url = reverse("feedback-export")
        response = self.client.get(url, {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment", response["Content-Disposition"])