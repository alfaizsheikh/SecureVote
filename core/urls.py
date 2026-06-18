from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome_view, name="welcome"),
    path("home/", views.home_view, name="home"),
    path("verify_otp/", views.verify_otp_view, name="verify_otp"),
    path("resend-otp/", views.resend_otp_view, name="resend_otp"),
    path("surveys/", views.survey_list_view, name="survey_list"),
    path("vote/<int:survey_id>/", views.vote_view, name="vote"),
    path("create-survey/", views.create_survey_view, name="create_survey"),
    path("results/", views.results_view, name="results"),
    path("results/<int:survey_id>/", views.results_view, name="results_detail"),
    path("admin-dashboard/", views.admin_dashboard_view, name="admin_dashboard"),
]

