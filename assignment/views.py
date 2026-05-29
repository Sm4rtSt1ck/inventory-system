from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.permissions import IsAdmin, IsAdminOrLabManager
from .models import Laboratory, Person, Assignment
from .serializers import LaboratorySerializer, PersonSerializer, AssignmentSerializer, AssignmentDetailSerializer


@extend_schema_view(
    list=extend_schema(tags=['Laboratories']),
    create=extend_schema(tags=['Laboratories']),
    retrieve=extend_schema(tags=['Laboratories']),
    update=extend_schema(tags=['Laboratories']),
    partial_update=extend_schema(tags=['Laboratories']),
    destroy=extend_schema(tags=['Laboratories']),
)
class LaboratoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin()]
        return [IsAuthenticated()]


@extend_schema_view(
    list=extend_schema(tags=['Persons']),
    create=extend_schema(tags=['Persons']),
    retrieve=extend_schema(tags=['Persons']),
    update=extend_schema(tags=['Persons']),
    partial_update=extend_schema(tags=['Persons']),
    destroy=extend_schema(tags=['Persons']),
)
class PersonViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin()]
        return [IsAuthenticated()]


@extend_schema_view(
    list=extend_schema(
        tags=['Assignments'],
        parameters=[
            OpenApiParameter('active', OpenApiTypes.BOOL, description='Filter only active assignments'),
        ],
    ),
    create=extend_schema(tags=['Assignments']),
    retrieve=extend_schema(tags=['Assignments']),
    update=extend_schema(tags=['Assignments']),
    partial_update=extend_schema(tags=['Assignments']),
)
class AssignmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Assignment.objects.select_related('equipment', 'laboratory', 'person').all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return AssignmentDetailSerializer
        return AssignmentSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsAuthenticated()]
        return [IsAdminOrLabManager()]

    def get_queryset(self):
        qs = super().get_queryset()
        active = self.request.query_params.get('active')
        if active is not None:
            if active.lower() == 'true':
                qs = qs.filter(date_to__isnull=True)
            elif active.lower() == 'false':
                qs = qs.filter(date_to__isnull=False)
        return qs
