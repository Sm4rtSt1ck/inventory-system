from rest_framework import serializers
from .models import Equipment, Component, EquipmentHistory


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('id', 'name', 'type')


class EquipmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentHistory
        fields = ('id', 'action', 'changed_by', 'timestamp')


class EquipmentSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Equipment
        fields = (
            'id', 'serial_number', 'name', 'model', 'type',
            'purchase_date', 'purpose', 'status', 'components',
        )


class EquipmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = (
            'serial_number', 'name', 'model', 'type',
            'purchase_date', 'purpose', 'status',
        )


class ComponentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('id', 'name', 'type')
