# UrbanCart Retail — Customer Feedback Management System (V1)

A lightweight, secure, and production-ready backend service designed to centralize customer feedback for UrbanCart Retail, featuring structured state transitions, rating/status filtering, and an on-demand CSV reporting utility.

---

## 🛠️ Technology Stack
* **Language:** Python 3.12
* **Framework:** Django 5.x
* **API Toolkit:** Django REST Framework (DRF)
* **Filtering:** `django-filter`
* **Database:** SQLite

---

## Key Features & Architecture
* **Single-Entity Data Model:** A flat, highly optimized `Feedback` model capturing customer details, ratings (1–5), comments, and status workflows.
* **Double-Validation Strategy:** Model-layer constraints (`MinValueValidator`, `MaxValueValidator`) protect the database storage layer, while serializer-level validation provides instant, consumer-friendly HTTP 400 responses at the request boundary.
* **Immutability Enforcement:** Public delete endpoints are intentionally omitted to ensure audit logs remain immutable for staff (system-level deletions are restricted exclusively to superusers via the internal Django Admin panel).
* **Advanced Query Filtering:** Integrated with `django-filter` to support fast, combined query parameters for `rating` and `status`.
* **On-Demand CSV Export:** A synchronous utility endpoint that compiles and streams feedback records into a clean CSV download file format.

---

## ⚙️ Installation & Local Setup

1. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Apply database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate

```


4. **Run the test suite:**
```bash
python manage.py test

```


5. **Create a superuser (for Django Admin access):**
```bash
python manage.py createsuperuser

```


6. **Run the development server:**
```bash
python manage.py runserver

```
## 🔌 API Endpoints Reference

> All API routes are versioned under `/api/v1/`[cite: 2].

### 📥 1. Submit Feedback
* **Method:** `POST`
* **Endpoint:** `/api/v1/feedback/`
* **Description:** Submit a new feedback entry.
* **Payload Fields:** `customer_name`, `email`, `rating` (1–5), `comment`

### 📋 2. List & Filter Feedback
* **Method:** `GET`
* **Endpoint:** `/api/v1/feedback/`
* **Description:** List all feedback with optional query parameters.
* **Example Query:** `/api/v1/feedback/?rating=5&status=Pending`

### 🔄 3. Mark as Reviewed
* **Method:** `PATCH`
* **Endpoint:** `/api/v1/feedback/{id}/review/`
* **Description:** Transition a record's status from *Pending* to *Reviewed*.
* **Payload:** None (Target ID in URL)

### 📊 4. Export Feedback (CSV)
* **Method:** `GET`
* **Endpoint:** `/api/v1/feedback/export/`
* **Description:** Download filtered or unfiltered feedback records as a CSV file.
* **Query Parameters:** Supports the same filters as the List endpoint (`rating`, `status`)

---
##  User Journey Workflow

1. **Submission:** Customer or staff submits feedback via the intake form.


2. **Validation & Storage:** Backend validates fields (ensuring valid email and 1–5 rating scale) and saves the record with a default status of `"Pending"`.


3. **Review & Filtering:** Staff members view the dashboard, apply query filters, or trigger a clean CSV export on-demand.


4. **State Transition:** Staff/Admin target a specific record via `PATCH /api/v1/feedback/{id}/review/` to transition its status to `"Reviewed"`, automatically refreshing the `updated_at` timestamp.



---
