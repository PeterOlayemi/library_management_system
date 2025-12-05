from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect

class UserRequiredMixin(AccessMixin):
    """Allow only authenticated non-staff users, with messages."""

    def dispatch(self, request, *args, **kwargs):
        # User not logged in
        if not request.user.is_authenticated:
            messages.warning(request, "You need to login to access this page.")
            return redirect("login")  # Redirect to your login URL

        # Staff user
        if request.user.is_staff:
            messages.error(request, "Staff cannot access this page.")
            return redirect("login")  # Or wherever you want

        # Otherwise, proceed normally
        return super().dispatch(request, *args, **kwargs)
