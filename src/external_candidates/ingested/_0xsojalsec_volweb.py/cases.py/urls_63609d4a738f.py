# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\cases\urls.py
from cases import views
from django.urls import path

urlpatterns = [
    path("cases/", views.cases, name="cases"),
    path("api/cases/", views.CasesApiView.as_view()),
    path("api/cases/<int:case_id>/", views.CaseApiView.as_view()),
    path("case/<int:case_id>/", views.case, name="case"),
]
