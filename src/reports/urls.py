from django.urls import path
from .views import create_report_view, report_view

app_name = "reports"

urlpatterns = [
    path("", report_view, name="report-view"),
    path("create/", create_report_view, name="create-report"),
]