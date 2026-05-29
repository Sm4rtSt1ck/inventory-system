from django.contrib import admin
from .models import Equipment, Component, EquipmentHistory


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 0


class EquipmentHistoryInline(admin.TabularInline):
    model = EquipmentHistory
    extra = 0
    readonly_fields = ('action', 'changed_by', 'timestamp')
    can_delete = False


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'type', 'status', 'purchase_date')
    list_filter = ('type', 'status')
    search_fields = ('name', 'serial_number', 'model')
    inlines = [ComponentInline, EquipmentHistoryInline]


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'equipment')
    list_filter = ('type',)
    raw_id_fields = ('equipment',)


@admin.register(EquipmentHistory)
class EquipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'action', 'changed_by', 'timestamp')
    readonly_fields = ('timestamp',)
