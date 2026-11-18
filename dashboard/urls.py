from django.urls import path
from .views import (
    RoleRedirectView,
    CreatorDashboardView,
    AdminDashboardView,
)

urlpatterns = [
    path('', RoleRedirectView.as_view(), name='role_redirect'),
    path('creator/', CreatorDashboardView.as_view(), name='creator_dashboard'),
    path('admin-panel/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
