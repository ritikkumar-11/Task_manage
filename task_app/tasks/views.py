from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.none()  # Dummy queryset for router compatibility

    def get_queryset(self):
        """
        Ensure users can only access their own tasks.
        Optionally filter tasks by 'completed' status, 'created_after', or 'created_before'.
        """
        # Filter tasks by the logged-in user
        queryset = Task.objects.filter(user=self.request.user)

        # Filter by 'completed' status (optional)
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            if completed.lower() not in ['true', 'false']:
                raise ValidationError("Invalid value for 'completed'. Use 'true' or 'false'.")
            completed = completed.lower() == 'true'
            queryset = queryset.filter(completed=completed)

        # Filter by 'created_after' date (optional)
        created_after = self.request.query_params.get('created_after', None)
        if created_after is not None:
            try:
                created_after_date = datetime.strptime(created_after, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date format for 'created_after'. Use 'YYYY-MM-DD'.")
            queryset = queryset.filter(created_at__date__gte=created_after_date)

        # Filter by 'created_before' date (optional)
        created_before = self.request.query_params.get('created_before', None)
        if created_before is not None:
            try:
                created_before_date = datetime.strptime(created_before, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date format for 'created_before'. Use 'YYYY-MM-DD'.")
            queryset = queryset.filter(created_at__date__lte=created_before_date)

        return queryset

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user as the task owner.
        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """
        Ensure users can only delete their own tasks.
        """
        if instance.user != self.request.user:
            return Response({'error': 'You do not have permission to delete this task'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def all_tasks(self, request):
        """
        Allow admin users to list all tasks.
        Non-admin users are denied access to this endpoint.
        """
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to view all tasks."},
                status=status.HTTP_403_FORBIDDEN
            )

        tasks = Task.objects.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)