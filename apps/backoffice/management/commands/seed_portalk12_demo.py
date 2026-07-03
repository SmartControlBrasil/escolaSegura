from datetime import date

from django.core.management.base import BaseCommand

from apps.backoffice.models import Guardian, SchoolUnit, Student, StudentGuardianLink


class Command(BaseCommand):
    help = 'Cria dados demonstrativos mínimos do PortalK12.'

    def handle(self, *args, **options):
        unit_center, _ = SchoolUnit.objects.update_or_create(
            slug='unidade-centro',
            defaults={
                'name': 'Unidade Centro',
                'legal_name': 'PortalK12 Unidade Centro Ltda.',
                'document': '12.345.678/0001-90',
                'email': 'centro@portalk12.test',
                'phone': '(11) 3000-1000',
                'address_line': 'Rua das Acácias, 120',
                'city': 'São Paulo',
                'state': 'SP',
                'is_active': True,
            },
        )
        unit_north, _ = SchoolUnit.objects.update_or_create(
            slug='unidade-norte',
            defaults={
                'name': 'Unidade Norte',
                'legal_name': 'PortalK12 Unidade Norte Ltda.',
                'document': '98.765.432/0001-10',
                'email': 'norte@portalk12.test',
                'phone': '(11) 3000-2000',
                'address_line': 'Avenida dos Ipês, 450',
                'city': 'São Paulo',
                'state': 'SP',
                'is_active': True,
            },
        )

        students_data = [
            (unit_center, 'Ana Beatriz Lima', 'CEN-0001', date(2014, 5, 12), '5º ano', '5º A'),
            (unit_center, 'Bruno Carvalho Reis', 'CEN-0002', date(2013, 9, 3), '6º ano', '6º B'),
            (unit_center, 'Clara Mendes Rocha', 'CEN-0003', date(2015, 2, 21), '4º ano', '4º A'),
            (unit_center, 'Daniel Nogueira Alves', 'CEN-0004', date(2012, 11, 8), '7º ano', '7º B'),
            (unit_north, 'Elisa Fernandes Costa', 'NOR-0001', date(2014, 7, 17), '5º ano', '5º C'),
            (unit_north, 'Felipe Martins Duarte', 'NOR-0002', date(2013, 1, 28), '6º ano', '6º A'),
            (unit_north, 'Gabriela Souza Pinto', 'NOR-0003', date(2015, 4, 9), '4º ano', '4º B'),
            (unit_north, 'Henrique Oliveira Santos', 'NOR-0004', date(2012, 8, 30), '7º ano', '7º A'),
        ]
        students = []
        for unit, full_name, code, birth_date, grade, classroom in students_data:
            student, _ = Student.objects.update_or_create(
                school_unit=unit,
                registration_code=code,
                defaults={
                    'full_name': full_name,
                    'birth_date': birth_date,
                    'grade_name': grade,
                    'classroom': classroom,
                    'status': Student.Status.ACTIVE,
                },
            )
            students.append(student)

        guardians_data = [
            ('Carla Lima', 'carla.lima@familia.test', '(11) 90000-0001', '111.111.111-11'),
            ('Roberto Reis', 'roberto.reis@familia.test', '(11) 90000-0002', '222.222.222-22'),
            ('Mariana Rocha', 'mariana.rocha@familia.test', '(11) 90000-0003', '333.333.333-33'),
            ('Patrícia Alves', 'patricia.alves@familia.test', '(11) 90000-0004', '444.444.444-44'),
            ('Sérgio Costa', 'sergio.costa@familia.test', '(11) 90000-0005', '555.555.555-55'),
            ('Helena Duarte', 'helena.duarte@familia.test', '(11) 90000-0006', '666.666.666-66'),
            ('Renata Pinto', 'renata.pinto@familia.test', '(11) 90000-0007', '777.777.777-77'),
            ('Márcio Santos', 'marcio.santos@familia.test', '(11) 90000-0008', '888.888.888-88'),
        ]
        guardians = []
        for full_name, email, phone, document in guardians_data:
            guardian, _ = Guardian.objects.update_or_create(
                document=document,
                defaults={
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                    'is_active': True,
                },
            )
            guardians.append(guardian)

        relationships = [
            StudentGuardianLink.Relationship.MOTHER,
            StudentGuardianLink.Relationship.FATHER,
            StudentGuardianLink.Relationship.MOTHER,
            StudentGuardianLink.Relationship.LEGAL_GUARDIAN,
            StudentGuardianLink.Relationship.FATHER,
            StudentGuardianLink.Relationship.MOTHER,
            StudentGuardianLink.Relationship.MOTHER,
            StudentGuardianLink.Relationship.FATHER,
        ]
        for student, guardian, relationship in zip(students, guardians, relationships):
            StudentGuardianLink.objects.update_or_create(
                student=student,
                guardian=guardian,
                defaults={
                    'relationship': relationship,
                    'can_authorize_exit': True,
                    'can_receive_notifications': True,
                    'can_approve_canteen_orders': relationship in {
                        StudentGuardianLink.Relationship.MOTHER,
                        StudentGuardianLink.Relationship.LEGAL_GUARDIAN,
                    },
                    'is_primary': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Seed PortalK12 demo criado com sucesso.'))
