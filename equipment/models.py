from django.db import models


class EquipmentType(models.TextChoices):
    COMPUTER = 'computer', 'Computer'
    LAPTOP = 'laptop', 'Laptop'
    SERVER = 'server', 'Server'
    OTHER = 'other', 'Other'


class EquipmentStatus(models.TextChoices):
    IN_USE = 'in_use', 'In Use'
    IN_REPAIR = 'in_repair', 'In Repair'
    DECOMMISSIONED = 'decommissioned', 'Decommissioned'


class Equipment(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=EquipmentType.choices)
    purchase_date = models.DateField()
    purpose = models.TextField(blank=True)
    status = models.CharField(
        max_length=50,
        choices=EquipmentStatus.choices,
        default=EquipmentStatus.IN_USE,
    )

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.serial_number})'


class ComponentType(models.TextChoices):
    MONITOR = 'monitor', 'Monitor'
    KEYBOARD = 'keyboard', 'Keyboard'
    MOUSE = 'mouse', 'Mouse'
    CPU = 'cpu', 'CPU'
    RAM = 'ram', 'RAM'
    HDD = 'hdd', 'HDD/SSD'
    GPU = 'gpu', 'GPU'
    OTHER = 'other', 'Other'


class Component(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=ComponentType.choices)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='components')

    class Meta:
        verbose_name = 'Component'
        verbose_name_plural = 'Components'
        ordering = ['type', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'


class EquipmentHistory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='history')
    action = models.TextField()
    changed_by = models.ForeignKey(
        'assignment.Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Equipment History'
        verbose_name_plural = 'Equipment History'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.equipment} — {self.timestamp:%Y-%m-%d %H:%M}'
