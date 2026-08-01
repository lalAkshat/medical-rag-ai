from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Authentication
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),

    # Upload Report
    path("upload/", views.upload_page, name="upload"),

    # Reports
    path("reports/", views.reports_page, name="reports"),

    # Delete Report
    path("delete/<int:report_id>/", views.delete_report, name="delete_report"),

    # AI Chat
    path("chat/<int:report_id>/", views.chat_page, name="chat"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )