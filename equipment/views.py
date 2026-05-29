from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.permissions import IsAdmin, IsAdminOrLabManager
from .models import Equipment, Component, EquipmentHistory
from .serializers import (
    EquipmentSerializer,
    EquipmentWriteSerializer,
    ComponentSerializer,
    ComponentCreateSerializer,
    EquipmentHistorySerializer,
)


@extend_schema_view(
    list=extend_schema(
        tags=['Equipment'],
        parameters=[
            OpenApiParameter('status', OpenApiTypes.STR, description='Filter by status'),
            OpenApiParameter('type', OpenApiTypes.STR, description='Filter by type'),
            OpenApiParameter('search', OpenApiTypes.STR, description='Search by name, model, serial_number'),
        ],
    ),
    create=extend_schema(tags=['Equipment']),
    retrieve=extend_schema(tags=['Equipment']),
    update=extend_schema(tags=['Equipment']),
    partial_update=extend_schema(tags=['Equipment']),
    destroy=extend_schema(tags=['Equipment']),
)
class EquipmentViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['name', 'model', 'serial_number']

    def get_queryset(self):
        qs = Equipment.objects.prefetch_related('components').all()
        status_filter = self.request.query_params.get('status')
        type_filter = self.request.query_params.get('type')
        if status_filter:
            qs = qs.filter(status=status_filter)
        if type_filter:
            qs = qs.filter(type=type_filter)
        return qs

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return EquipmentWriteSerializer
        return EquipmentSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return [IsAdmin()]
        if self.action in ('update', 'partial_update'):
            return [IsAdminOrLabManager()]
        return [IsAuthenticated()]

    @extend_schema(tags=['Equipment'], responses={200: ComponentSerializer(many=True)})
    @action(detail=True, methods=['get'], url_path='components')
    def list_components(self, request, pk=None):
        equipment = self.get_object()
        serializer = ComponentSerializer(equipment.components.all(), many=True)
        return Response(serializer.data)

    @extend_schema(tags=['Equipment'], request=ComponentCreateSerializer, responses={201: ComponentSerializer})
    @list_components.mapping.post
    def add_component(self, request, pk=None):
        self._check_admin(request)
        equipment = self.get_object()
        serializer = ComponentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        component = serializer.save(equipment=equipment)
        return Response(ComponentSerializer(component).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=['Equipment'], responses={204: None})
    @action(
        detail=True,
        methods=['delete'],
        url_path='components/(?P<comp_id>[^/.]+)',
        permission_classes=[IsAdmin],
    )
    def remove_component(self, request, pk=None, comp_id=None):
        equipment = self.get_object()
        component = Component.objects.filter(pk=comp_id, equipment=equipment).first()
        if component is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        component.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(tags=['Equipment'], responses={200: EquipmentHistorySerializer(many=True)})
    @action(detail=True, methods=['get'], url_path='history', permission_classes=[IsAuthenticated])
    def history(self, request, pk=None):
        equipment = self.get_object()
        serializer = EquipmentHistorySerializer(equipment.history.all(), many=True)
        return Response(serializer.data)

    def _check_admin(self, request):
        if not IsAdmin().has_permission(request, self):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
