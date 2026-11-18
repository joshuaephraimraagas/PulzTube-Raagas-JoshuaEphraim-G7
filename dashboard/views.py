from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from accounts.models import CustomUser
from .models import ContentItem, ChannelStat

class RoleRedirectView(LoginRequiredMixin, View):
    """
    Directs authenticated users to their specific role dashboard immediately after login:
    - ADMIN -> /dashboard/admin/
    - CREATOR -> /dashboard/creator/
    """
    def get(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.ADMIN or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('creator_dashboard')


class CreatorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Creator Dashboard:
    - Provides a centralized home screen for content creators.
    - Displays channel info, pipeline breakdown across 7 stages, and upcoming items.
    - Security: Non-creators cannot access by URL.
    """
    template_name = 'dashboard/creator_dashboard.html'

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.Role.CREATOR or user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        messages.warning(
            self.request,
            "Access restricted: As an Administrator, you have been redirected to the Admin Dashboard."
        )
        return redirect('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Pipeline items for this creator
        items = ContentItem.objects.filter(user=user)
        
        # Pipeline status counts (7 defined stages)
        status_counts = {
            'IDEA': items.filter(status=ContentItem.Status.IDEA).count(),
            'PLANNING': items.filter(status=ContentItem.Status.PLANNING).count(),
            'RECORDING': items.filter(status=ContentItem.Status.RECORDING).count(),
            'EDITING': items.filter(status=ContentItem.Status.EDITING).count(),
            'READY': items.filter(status=ContentItem.Status.READY).count(),
            'SCHEDULED': items.filter(status=ContentItem.Status.SCHEDULED).count(),
            'PUBLISHED': items.filter(status=ContentItem.Status.PUBLISHED).count(),
        }
        
        # Latest recorded channel stats (Sprint 2 placeholder)
        latest_stat = ChannelStat.objects.filter(user=user).first()
        
        context['status_counts'] = status_counts
        context['total_items'] = items.count()
        context['latest_stat'] = latest_stat
        context['recent_items'] = items[:5]
        return context


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Admin Dashboard:
    - Provides system overview, user count, role distribution, and management metrics.
    - Security: Creators cannot open this dashboard by typing its URL.
    """
    template_name = 'dashboard/admin_dashboard.html'

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.Role.ADMIN or user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        # Explicit error message when a creator tries to access the admin dashboard URL
        messages.error(
            self.request,
            "Access Denied: You do not have permission to view the Administrator Dashboard."
        )
        return redirect('creator_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_users = CustomUser.objects.all().order_by('-date_joined')
        
        context['total_users'] = all_users.count()
        context['total_creators'] = all_users.filter(role=CustomUser.Role.CREATOR).count()
        context['total_admins'] = all_users.filter(role=CustomUser.Role.ADMIN).count()
        context['recent_users'] = all_users[:10]
        return context
