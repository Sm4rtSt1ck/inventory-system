from django.urls import path
from .views import LoginView, EquipmentListView, EquipmentDetailView, AssignmentsView, LaboratoriesView, PersonsView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', EquipmentListView.as_view(), name='equipment-list'),
    path('equipment/<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail'),
    path('assignments/', AssignmentsView.as_view(), name='assignments'),
    path('laboratories/', LaboratoriesView.as_view(), name='laboratories'),
    path('persons/', PersonsView.as_view(), name='persons'),
]
