from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

import os


class Account(User):
    name = models.CharField(verbose_name='Nome', max_length=100)
    cellphone = models.CharField(verbose_name="Telefone", max_length=15, blank=True, null=False, default="")
    city = models.CharField(verbose_name="Cidade", max_length=50)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.name

