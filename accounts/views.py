from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View

from .models import CustomUser
from .forms import (
    CustomUserRegistrationForm,
    UserProfileUpdateForm,
    CustomLoginForm,
)

class SignUpView(CreateView):
    """
    Handles new user registration with strict validation:
    - Required fields, valid email format, unique username and unique email.
    - Password hashing via Django's auth system.
    - Clear feedback messages.
    """
    form_class = CustomUserRegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Redirect logged-in users away from signup page
        if request.user.is_authenticated:
            return redirect('role_redirect')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        # Default role for all newly registered users is Content Creator
        user.role = CustomUser.Role.CREATOR
        user.save()
        messages.success(
            self.request,
            f"Account created successfully for {user.username}! You can now log in."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Registration failed. Please check the form errors below."
        )
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    """
    Handles user authentication with clear error and success messages.
    """
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        display_name = user.first_name if user.first_name else user.username
        messages.success(self.request, f"Welcome back, {display_name}!")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Invalid username or password. Please verify your credentials and try again."
        )
        return super().form_invalid(form)


class CustomLogoutView(View):
    """
    Logs out the user, ends the session, and redirects to the login page with a message.
    """
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        return redirect('login')


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Allows a logged-in user to view their own profile information.
    Strictly scoped to request.user.
    """
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Allows a logged-in user to update their own profile details.
    Users can ONLY view and edit their own profile.
    """
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Guarantee that the user can only edit their own profile object
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Could not update profile. Please correct the errors below.")
        return super().form_invalid(form)
