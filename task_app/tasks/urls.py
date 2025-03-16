from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet

# Create a router
router = DefaultRouter()

# Register the TaskViewSet with an explicit basename (optional)
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # Include the router's URLs
    path('api/', include(router.urls)),
]