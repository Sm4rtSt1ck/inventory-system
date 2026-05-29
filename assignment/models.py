from django.db import models


class Laboratory(models.Model):
    name = models.CharField(max_length=255)
    room = models.CharField(max_length=50)
    building = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Laboratory'
        verbose_name_plural = 'Laboratories'
        ordering = ['building', 'room']

    def __str__(self):
        return f'{self.name} ({self.building}, room {self.room})'


class Person(models.Model):
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.role})'


class Assignment(models.Model):
    equipment = models.ForeignKey(
        'equipment.Equipment',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='assignments')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='assignments')
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        ordering = ['-date_from']

    def __str__(self):
        status = 'active' if self.date_to is None else f'until {self.date_to}'
        return f'{self.equipment} → {self.laboratory} ({status})'

    @property
    def is_active(self):
        return self.date_to is None
