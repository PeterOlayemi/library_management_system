from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect

class StaffRequiredMixin(AccessMixin):
    """Allow only staff users, with messages."""

    def dispatch(self, request, *args, **kwargs):
        # User not logged in
        if not request.user.is_authenticated:
            messages.warning(request, "You need to login to access this page.")
            return redirect("login")  # Replace with your login URL

        # Non-staff user
        if not request.user.is_staff:
            messages.error(request, "You must be a staff member to access this page.")
            return redirect("login")  # Or a safe page for normal users

        # Otherwise, proceed normally
        return super().dispatch(request, *args, **kwargs)
