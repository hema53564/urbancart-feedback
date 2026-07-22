import csv
from django.http import HttpResponse

def export_feedback_to_csv(queryset):
    """
    Generates a downloadable CSV file from a filtered feedback queryset.
    """
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="feedback_export.csv"'},
    )
    
    writer = csv.writer(response)
    
    # FIXED: Added the actual column headers (the original document had this empty)
    writer.writerow([
        "ID", 
        "Customer Name", 
        "Email", 
        "Rating", 
        "Comment", 
        "Status", 
        "Date Submitted"
    ])
    
    # FIXED: Added the actual data fields mapped to the model (the original document had this empty)
    for feedback in queryset:
        writer.writerow([
            feedback.id,
            feedback.customer_name,
            feedback.email,
            feedback.rating,
            feedback.comment,
            feedback.status,
            feedback.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])
        
    return response