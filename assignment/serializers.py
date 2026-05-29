from rest_framework import serializers
from .models import Laboratory, Person, Assignment


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = ('id', 'name', 'room', 'building')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'full_name', 'role', 'email')


class AssignmentSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'equipment', 'laboratory', 'person', 'date_from', 'date_to', 'is_active')

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        if date_from and date_to and date_to < date_from:
            raise serializers.ValidationError('date_to must be after date_from')
        return data


class AssignmentDetailSerializer(AssignmentSerializer):
    laboratory = LaboratorySerializer(read_only=True)
    person = PersonSerializer(read_only=True)
