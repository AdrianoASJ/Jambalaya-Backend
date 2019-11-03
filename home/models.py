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


class Hotel(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,
                             verbose_name="Usuario Da Reserva", blank=True, null=True)
    name = models.CharField(verbose_name='Nome do Hotel', max_length=255)
    qtd_criancas = models.CharField(verbose_name="Quantidade de Crianças", max_length=2, blank=True, null=True)
    qtd_adultos = models.CharField(verbose_name="Quantidade de Adultos", max_length=2, blank=True, null=True)
    qtd_bebes = models.CharField(verbose_name="Quantidade de Bebes", max_length=2, blank=True, null=True)
    checkin = models.CharField(verbose_name="Data de Entrada (Checkin)", max_length=100)
    checkout = models.CharField(verbose_name="Data de Saida (Checkout)", max_length=100)

    class Meta:
        verbose_name = "Reserva de Hotel"
        verbose_name_plural = "Reserva de Hotéis"

    def __str__(self):
        return self.name
