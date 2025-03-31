from django import forms
from . models import *

class AddMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialObj
        fields = '__all__'
        widgets = {
            'contrato': forms.Select(attrs={
                'class': 'form-control form-control-sm',
                'style': 'width: 400px;',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3,
                'placeholder': 'Descrição do material...',
                'style': 'width: 570px;',
            }),
            'data': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AddMaterialForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class TipoMaterForm(forms.ModelForm):
    class Meta:
        model = MaterialTipo
        fields = '__all__'
        widgets = {
            'material_obj': forms.Select(attrs={
                'class': 'form-control form-control-sm',
                'style': 'width: 300px;',
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Marca do material...',
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Modelo do material...',
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Quantidade...',
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3,
                'placeholder': 'Observações...',
            }),
            'garantia': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Garantia...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(TipoMaterForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class SaidaMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialSaida
        fields = '__all__'
        widgets = {
            'unidade': forms.Select(attrs={
            'style': 'width: 500px',
            }),
            'departamento': forms.Select(attrs={
            'style': 'width: 500px',
            }),
            'divisao_field': forms.Select(attrs={
            'style': 'width: 500px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SaidaMaterialForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class AddContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'
        widgets = {
            'nome_contrato': forms.TextInput(attrs={
                'style': 'width: 600px',
            }),
            'descricao_contr': forms.Textarea(attrs={
                'rows': 4,
                'style': 'width: 600px',
            }),
            'data_abert': forms.DateInput(attrs={
                'type': 'date',
                'style': 'width: 300px;',
            }),
            'num_contrato': forms.TextInput(attrs={
                'style': 'width: 600px',
            }),
            'data_renov': forms.DateInput(attrs={
                'type': 'date',
                'style': 'width: 300px',
            }),
             'data_fim': forms.DateInput(attrs={
                'type': 'date',
                'style': 'width: 300px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AddContratoForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class AddUnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = '__all__'
        widgets = {
            'unidade': forms.TextInput(attrs={
                'style': 'width: 500px',
            }),
            'departamento': forms.TextInput(attrs={
                'style': 'width: 500px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AddUnidadeForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class AddDepartForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'style': 'width: 500px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AddDepartForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class AddDivisãoForm(forms.ModelForm):
    class Meta:
        model = Divisao
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'style': 'width: 500px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AddDivisãoForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class EditarMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialTipo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditarMaterialForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'
            self.fields[i].widget.attrs['style'] = 'width: 500px'




