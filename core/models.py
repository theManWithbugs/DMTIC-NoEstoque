from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import os

class MaterialObj(models.Model): 
    marca = models.CharField(max_length=20, blank=False, null=False, default='', verbose_name='Marca ')
    modelo = models.CharField(max_length=20, blank=False,  null=False, verbose_name='Modelo ')
    contrato = models.CharField(max_length=20, blank=False, null=False, verbose_name='Contrato ')
    garantia = models.CharField(max_length=20, blank=False, null=False, verbose_name='Garantia ')
    observacao = models.CharField(max_length=400, blank=True, null=True, verbose_name='Observações ')

    def __str__(self):
        return f"{self.marca}, {self.modelo}, {self.contrato}, {self.garantia}, {self.observacao}"

