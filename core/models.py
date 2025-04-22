from django.db import models
from datetime import date

class MaterialObj(models.Model): 
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Contrato')
    descricao = models.CharField(max_length=400, blank=True, null=True, verbose_name='Descrição ')
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f" -{self.contrato}- "
    
class MaterialTipo(models.Model):
    material_obj = models.ForeignKey('MaterialObj', on_delete=models.CASCADE, related_name='tipo_obj', verbose_name='Contrato')
    saida_obj = models.ForeignKey('MaterialSaida', on_delete=models.CASCADE, related_name='saida_obj', blank=True, null=True, verbose_name='Saida')
    marca = models.CharField(max_length=20, blank=False, null=False, default='', verbose_name='Marca ')
    modelo = models.CharField(max_length=80, blank=False, null=False, verbose_name='Modelo ')
    quantidade = models.IntegerField(blank=False, null=False, verbose_name='Quantidade ')
    observacao = models.CharField(max_length=400, blank=True, null=True, verbose_name='Observações ')
    garantia = models.CharField(max_length=20, blank=False, null=False, verbose_name='Garantia ')

    def __str__(self):
        return f"-{self.marca}- ( {self.modelo} ) ( {self.quantidade} )"

class MaterialSaida(models.Model):
    unidade = models.ForeignKey('Unidade', on_delete=models.CASCADE, null=False, blank=False, related_name='materiais_unidade', verbose_name='Unidade')
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, null=False, blank=False, related_name='materiais_departamento', verbose_name='Departamento')
    divisao_field = models.ForeignKey('Divisao', on_delete=models.CASCADE, blank=False, null=False, related_name='materiais_divisao', verbose_name='Divisão ')

    def __str__(self):
        return f"-{self.unidade}- ({self.departamento} ({self.divisao_field}))"

class Contrato(models.Model):
    nome_contrato = models.CharField(max_length=60, blank=True, null=True, verbose_name='Nome do contrato ')
    descricao_contr = models.CharField(max_length=400, blank=False, null=False, default='', verbose_name='Descrição do contrato ')
    num_contrato = models.CharField(blank=False, null=False, max_length=80, verbose_name='Número do contrato ')
    data_abert = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"-{self.nome_contrato}- ( {self.num_contrato} )"

class Unidade(models.Model):
    unidade = models.CharField(max_length=30, verbose_name='Nova Unidade ')

    def __str__(self):
        return self.unidade

class Departamento(models.Model):
    nome = models.CharField(max_length=30, verbose_name='Adicionar Departamento ')
    unidade = models.ForeignKey('Unidade', on_delete=models.CASCADE, related_name='departamentos', verbose_name='A qual unidade pertence? ')  

    def __str__(self):
        return f"{self.nome} ({self.unidade})"

class Divisao(models.Model):
    nome = models.CharField(max_length=80, verbose_name='Adicionar Divisão ')
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, related_name='divisoes', verbose_name='A qual departamento pertence? ')  

    def __str__(self):
        return f"{self.nome} ({self.departamento})"