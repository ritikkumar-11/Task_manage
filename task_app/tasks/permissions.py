from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Admin users can perform any action.
    - Non-admin users cannot view the full list of all users' tasks.
    """

    def has_permission(self, request, view):
        # Allow admin users to access the full list of tasks
        if request.user and request.user.is_staff:
            return True

        # Deny access to non-admin users for unsafe methods or specific views
        if view.action == 'all_tasks':  # Assuming 'all_tasks' is the custom action
            return False

        # Allow authenticated users to access their own tasks
        return request.user and request.user.is_authenticated