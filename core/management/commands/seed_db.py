from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Seed the database with initial test data'

    @transaction.atomic
    def handle(self, *args, **options):
        from assignment.models import Laboratory, Person
        from auth_app.models import User
        from equipment.models import Equipment, Component, EquipmentType, EquipmentStatus, ComponentType
        from assignment.models import Assignment

        self.stdout.write('Clearing existing data...')
        Assignment.objects.all().delete()
        Component.objects.all().delete()
        Equipment.objects.all().delete()
        User.objects.all().delete()
        Person.objects.all().delete()
        Laboratory.objects.all().delete()

        self.stdout.write('Creating laboratories...')
        lab1 = Laboratory.objects.create(name='Computer Science Lab', room='101', building='Main Building')
        lab2 = Laboratory.objects.create(name='Network Technologies Lab', room='205', building='Tech Block')
        lab3 = Laboratory.objects.create(name='Server Room', room='B01', building='Main Building')

        self.stdout.write('Creating persons...')
        p1 = Person.objects.create(full_name='Иван Петров', role='lab_manager', email='petrov@university.edu')
        p2 = Person.objects.create(full_name='Мария Сидорова', role='lab_manager', email='sidorova@university.edu')
        p3 = Person.objects.create(full_name='Алексей Козлов', role='teacher', email='kozlov@university.edu')
        p4 = Person.objects.create(full_name='Елена Новикова', role='teacher', email='novikova@university.edu')
        p5 = Person.objects.create(full_name='Дмитрий Соколов', role='teacher', email='sokolov@university.edu')

        self.stdout.write('Creating users...')
        admin = User.objects.create_superuser(
            username='admin', email='admin@university.edu',
            password='admin123', role='admin',
        )
        manager = User.objects.create_user(
            username='manager', email='manager@university.edu',
            password='manager123', role='lab_manager', person=p1,
        )
        teacher = User.objects.create_user(
            username='teacher', email='teacher@university.edu',
            password='teacher123', role='teacher', person=p3,
        )

        self.stdout.write('Creating equipment...')
        equipment_data = [
            ('SN-001', 'Dell OptiPlex 7090', 'OptiPlex 7090', EquipmentType.COMPUTER, date(2022, 3, 15), EquipmentStatus.IN_USE),
            ('SN-002', 'Dell OptiPlex 7090', 'OptiPlex 7090', EquipmentType.COMPUTER, date(2022, 3, 15), EquipmentStatus.IN_USE),
            ('SN-003', 'HP ProBook 450 G9', 'ProBook 450 G9', EquipmentType.LAPTOP, date(2023, 6, 1), EquipmentStatus.IN_USE),
            ('SN-004', 'HP ProBook 450 G9', 'ProBook 450 G9', EquipmentType.LAPTOP, date(2023, 6, 1), EquipmentStatus.IN_REPAIR),
            ('SN-005', 'Dell PowerEdge R750', 'PowerEdge R750', EquipmentType.SERVER, date(2021, 11, 20), EquipmentStatus.IN_USE),
            ('SN-006', 'Dell PowerEdge R750', 'PowerEdge R750', EquipmentType.SERVER, date(2021, 11, 20), EquipmentStatus.IN_USE),
            ('SN-007', 'Lenovo ThinkStation P620', 'ThinkStation P620', EquipmentType.COMPUTER, date(2023, 1, 10), EquipmentStatus.IN_USE),
            ('SN-008', 'Apple MacBook Pro 14', 'MacBook Pro 14', EquipmentType.LAPTOP, date(2024, 2, 5), EquipmentStatus.IN_USE),
            ('SN-009', 'Cisco Catalyst 9300', 'Catalyst 9300', EquipmentType.OTHER, date(2020, 8, 30), EquipmentStatus.DECOMMISSIONED),
            ('SN-010', 'Raspberry Pi 4 Cluster', 'Pi 4 8GB', EquipmentType.OTHER, date(2022, 9, 12), EquipmentStatus.IN_USE),
        ]
        equipment_list = []
        for sn, name, model, etype, pdate, status in equipment_data:
            eq = Equipment.objects.create(
                serial_number=sn, name=name, model=model,
                type=etype, purchase_date=pdate, status=status,
                purpose=f'Used in {lab1.name} for teaching purposes',
            )
            equipment_list.append(eq)

        self.stdout.write('Creating components...')
        for eq in equipment_list[:7]:
            Component.objects.create(name='Samsung 27" Monitor', type=ComponentType.MONITOR, equipment=eq)
            Component.objects.create(name='Logitech K120 Keyboard', type=ComponentType.KEYBOARD, equipment=eq)
            Component.objects.create(name='Logitech M100 Mouse', type=ComponentType.MOUSE, equipment=eq)

        for eq in equipment_list[:2]:
            Component.objects.create(name='Intel Core i7-11700', type=ComponentType.CPU, equipment=eq)
            Component.objects.create(name='Samsung DDR4 16GB', type=ComponentType.RAM, equipment=eq)
            Component.objects.create(name='WD Blue 512GB SSD', type=ComponentType.HDD, equipment=eq)

        self.stdout.write('Creating assignments...')
        Assignment.objects.create(
            equipment=equipment_list[0], laboratory=lab1, person=p1,
            date_from=date(2022, 4, 1), date_to=None,
        )
        Assignment.objects.create(
            equipment=equipment_list[1], laboratory=lab1, person=p3,
            date_from=date(2022, 4, 1), date_to=None,
        )
        Assignment.objects.create(
            equipment=equipment_list[2], laboratory=lab2, person=p2,
            date_from=date(2023, 7, 1), date_to=None,
        )
        Assignment.objects.create(
            equipment=equipment_list[3], laboratory=lab2, person=p4,
            date_from=date(2023, 7, 1), date_to=date(2024, 12, 31),
        )
        Assignment.objects.create(
            equipment=equipment_list[4], laboratory=lab3, person=p1,
            date_from=date(2021, 12, 1), date_to=None,
        )
        Assignment.objects.create(
            equipment=equipment_list[5], laboratory=lab3, person=p2,
            date_from=date(2021, 12, 1), date_to=None,
        )
        Assignment.objects.create(
            equipment=equipment_list[6], laboratory=lab1, person=p5,
            date_from=date(2023, 2, 1), date_to=None,
        )
        Assignment.objects.create(
            equipment=equipment_list[7], laboratory=lab2, person=p3,
            date_from=date(2024, 3, 1), date_to=None,
        )
        Assignment.objects.create(
            equipment=equipment_list[8], laboratory=lab1, person=p4,
            date_from=date(2020, 9, 1), date_to=date(2023, 8, 31),
        )
        Assignment.objects.create(
            equipment=equipment_list[9], laboratory=lab3, person=p5,
            date_from=date(2022, 10, 1), date_to=None,
        )

        self.stdout.write(self.style.SUCCESS(
            '\nDatabase seeded successfully!\n'
            'Users created:\n'
            '  admin / admin123  (role: admin)\n'
            '  manager / manager123  (role: lab_manager)\n'
            '  teacher / teacher123  (role: teacher)\n'
        ))
