from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LaboratoryViewSet, PersonViewSet, AssignmentViewSet

router = DefaultRouter()
router.register('laboratories', LaboratoryViewSet, basename='laboratory')
router.register('persons', PersonViewSet, basename='person')
router.register('assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
]
