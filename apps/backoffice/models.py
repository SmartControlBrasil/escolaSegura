from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        abstract = True


class SchoolUnit(TimeStampedModel):
    name = models.CharField('nome', max_length=160)
    slug = models.SlugField('slug', max_length=180, unique=True)
    legal_name = models.CharField('razão social', max_length=180, blank=True)
    document = models.CharField('documento', max_length=32, blank=True)
    email = models.EmailField('e-mail', blank=True)
    phone = models.CharField('telefone', max_length=32, blank=True)
    address_line = models.CharField('endereço', max_length=220, blank=True)
    city = models.CharField('cidade', max_length=120)
    state = models.CharField('estado', max_length=2)
    is_active = models.BooleanField('ativo', default=True)

    class Meta:
        verbose_name = 'Unidade escolar'
        verbose_name_plural = 'Unidades escolares'
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Ativo'
        INACTIVE = 'INACTIVE', 'Inativo'
        TRANSFERRED = 'TRANSFERRED', 'Transferido'

    school_unit = models.ForeignKey(
        SchoolUnit,
        verbose_name='unidade escolar',
        related_name='students',
        on_delete=models.PROTECT,
    )
    full_name = models.CharField('nome completo', max_length=180)
    registration_code = models.CharField('código de matrícula', max_length=50)
    birth_date = models.DateField('data de nascimento', blank=True, null=True)
    grade_name = models.CharField('série', max_length=80, blank=True)
    classroom = models.CharField('turma/sala', max_length=80, blank=True)
    status = models.CharField('status', max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['full_name']
        constraints = [
            models.UniqueConstraint(
                fields=['school_unit', 'registration_code'],
                name='backoffice_student_unique_registration_per_unit',
            ),
        ]

    def __str__(self):
        return self.full_name


class Guardian(TimeStampedModel):
    full_name = models.CharField('nome completo', max_length=180)
    email = models.EmailField('e-mail', blank=True)
    phone = models.CharField('telefone', max_length=32)
    document = models.CharField('documento', max_length=32, blank=True)
    is_active = models.BooleanField('ativo', default=True)

    class Meta:
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class StudentGuardianLink(TimeStampedModel):
    class Relationship(models.TextChoices):
        FATHER = 'FATHER', 'Pai'
        MOTHER = 'MOTHER', 'Mãe'
        GRANDPARENT = 'GRANDPARENT', 'Avô/Avó'
        LEGAL_GUARDIAN = 'LEGAL_GUARDIAN', 'Responsável legal'
        OTHER = 'OTHER', 'Outro'

    student = models.ForeignKey(
        Student,
        verbose_name='aluno',
        related_name='guardian_links',
        on_delete=models.CASCADE,
    )
    guardian = models.ForeignKey(
        Guardian,
        verbose_name='responsável',
        related_name='student_links',
        on_delete=models.CASCADE,
    )
    relationship = models.CharField('parentesco', max_length=20, choices=Relationship.choices)
    can_authorize_exit = models.BooleanField('pode autorizar saída', default=True)
    can_receive_notifications = models.BooleanField('pode receber notificações', default=True)
    can_approve_canteen_orders = models.BooleanField('pode aprovar pedidos da cantina', default=False)
    is_primary = models.BooleanField('responsável principal', default=False)

    class Meta:
        verbose_name = 'Vínculo aluno-responsável'
        verbose_name_plural = 'Vínculos aluno-responsável'
        ordering = ['student__full_name', 'guardian__full_name']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'guardian'],
                name='backoffice_unique_student_guardian_link',
            ),
        ]

    def __str__(self):
        return f'{self.student} - {self.guardian}'
