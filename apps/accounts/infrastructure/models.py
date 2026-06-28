import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Proprietário'
        ADMIN = 'admin', 'Administrador'
        MANAGER = 'manager', 'Gestor'
        OPERATOR = 'operator', 'Operador'
        VIEWER = 'viewer', 'Leitura'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.OPERATOR)
    phone = models.CharField(max_length=32, blank=True)
    must_change_password = models.BooleanField(default=False)

    @property
    def is_owner_or_admin(self):
        return self.is_superuser or self.role in {self.Role.OWNER, self.Role.ADMIN}
