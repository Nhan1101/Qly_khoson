from django.urls import path

from .views import landing_page_view, login_page_view

urlpatterns = [
    path("", landing_page_view, name="landing-page"),
    path("login/", login_page_view, name="login-page"),
]
