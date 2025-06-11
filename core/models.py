from django.db import models
from django.utils import timezone

class MaterialObj(models.Model): 
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Contrato')
    descricao = models.CharField(max_length=400, blank=True, null=True, verbose_name='Descrição ')
    data = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.contrato}"
    
class MaterialTipo(models.Model):
    material_obj = models.ForeignKey('MaterialObj', on_delete=models.CASCADE, related_name='tipo_obj', verbose_name='Contrato')
    saida_obj = models.ForeignKey('MaterialSaida', on_delete=models.CASCADE, related_name='saida_obj', blank=True, null=True, verbose_name='Saida')
    marca = models.CharField(max_length=20, blank=False, null=False, default='', verbose_name='Marca ')
    modelo = models.CharField(max_length=80, blank=False, null=False, verbose_name='Modelo ')
    n_serie = models.CharField(blank=False, null=False, verbose_name='Número de série', max_length=30, unique=True)
    patrimonio = models.CharField(blank=True, null=True, max_length=40, verbose_name='Patrimonio', unique=True)
    observacao = models.CharField(max_length=450, blank=True, null=True, verbose_name='Observações')
    garantia = models.CharField(max_length=20, blank=False, null=False, verbose_name='Garantia')
    data_cria = models.DateField(auto_now_add=True, verbose_name='Data de criação')

    def __str__(self):
        return f"-{self.marca}- ( {self.modelo} )"

    def get_complete_object(self):
        return {
            "Material": str(self.material_obj),
            "Saida": str(self.saida_obj) if self.saida_obj else None,
            "Marca": self.marca,
            "Modelo": self.modelo,
            "Número de série": self.n_serie,
            "Patrimonio": self.patrimonio,
            "Observação": self.observacao,
            "Garantia": self.garantia,
        }

class MaterialSaida(models.Model):
    unidade = models.ForeignKey('Unidade', on_delete=models.CASCADE, null=False, blank=False, related_name='materiais_unidade', verbose_name='Unidade')
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, null=False, blank=False, related_name='materiais_departamento', verbose_name='Departamento')
    divisao_field = models.ForeignKey(
        'Divisao',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='materiais_divisao',
        verbose_name='Divisão',
    )
    n_processo = models.CharField(max_length=40, verbose_name='Número do processo(SEI)', unique=True, blank=True, null=True)
    data_saida = models.DateField(default=timezone.now)

    def __str__(self):
        return f"-{self.unidade}- ({self.departamento} ({self.divisao_field}))"

class Contrato(models.Model):
    nome_contrato = models.CharField(max_length=60, blank=False, null=False, verbose_name='Nome do contrato ')
    descricao_contr = models.CharField(max_length=400, blank=False, null=False, default='', verbose_name='Descrição do contrato ')
    num_contrato = models.CharField(blank=False, null=False, max_length=80, verbose_name='Número do contrato ')
    data_abert = models.DateField(default=timezone.now)

    def __str__(self):
        return f"-{self.nome_contrato}- ( {self.num_contrato} )"

class Unidade(models.Model):
    unidade = models.CharField(
        max_length=30,
        verbose_name='Nova Unidade',
        unique=True,
        error_messages={'unique': "Error: Já existe uma unidade com esse nome."},
    )

    def __str__(self):
        return self.unidade

class Departamento(models.Model):
    nome = models.CharField(
        max_length=30,
        verbose_name='Adicionar Departamento',
        error_messages={'unique': "Error: Já existe um departamento com esse nome."}
    )
    unidade = models.ForeignKey(
        'Unidade',
        on_delete=models.CASCADE,
        related_name='departamentos',
        verbose_name='A qual unidade pertence?'
    )

    class Meta:
        unique_together = ('nome', 'unidade')

    def __str__(self):
        return f"{self.nome} ({self.unidade})"

class Divisao(models.Model):
    nome = models.CharField(
        max_length=80,
        verbose_name='Adicionar Divisão',
        error_messages={'unique': "Error: Já existe uma divisão com esse nome."}
    )
    departamento = models.ForeignKey(
        'Departamento',
        on_delete=models.CASCADE,
        related_name='divisoes',
        verbose_name='A qual departamento pertence?'
    )

    class Meta:
        unique_together = ('nome', 'departamento')

    def __str__(self):
        return f"{self.nome} {self.departamento}"
    
class HistoricoUser(models.Model):
    nome_user = models.CharField(max_length=30, blank=True, null=True)
    acao_realizada = models.CharField(max_length=50)
    modelo_item = models.CharField(max_length=80)
    data = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.nome_user} {self.data}"

    