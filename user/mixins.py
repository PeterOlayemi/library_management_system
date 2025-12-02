from django.contrib.auth.mixins import AccessMixin

class UserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.is_staff:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
