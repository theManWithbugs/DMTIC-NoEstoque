from django import forms
from . models import *

class AddMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialObj
        fields = '__all__'
        widgets = {
            'marca': forms.TextInput(attrs={
                'style': 'width: 300px',
            }),
            'modelo': forms.TextInput(attrs={
                'style': 'width: 300px;',
            }),
            'garantia': forms.TextInput(attrs={
                'style': 'width: 300px',
            }),
            'observacao': forms.Textarea(attrs={
                'rows': 4,
                'style': 'width: 600px',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AddMaterialForm, self).__init__(*args, **kwargs)
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




