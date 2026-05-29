from django.contrib import admin
from .models import Laboratory, Person, Assignment


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'building')
    search_fields = ('name', 'building')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'email')
    list_filter = ('role',)
    search_fields = ('full_name', 'email')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'laboratory', 'person', 'date_from', 'date_to')
    list_filter = ('laboratory',)
    raw_id_fields = ('equipment', 'person')
