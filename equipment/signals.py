from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='equipment.Equipment')
def log_equipment_change(sender, instance, created, **kwargs):
    from .models import EquipmentHistory

    action = f'Created: {instance.name}' if created else (
        f'Updated: status={instance.status}, name={instance.name}'
    )
    EquipmentHistory.objects.create(equipment=instance, action=action, changed_by=None)
