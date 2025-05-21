from django import forms
from . models import *

class AddMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialObj
        fields = '__all__'
        exclude = ['data']
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
        exclude = ['saida_obj']
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
            'n_serie': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Númeração do item..',
            }),
            'patrimonio': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Patrimonio do item...',
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
        exclude = ['data_saida']

    def __init__(self, *args, **kwargs):
        super(SaidaMaterialForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class AddContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'
        exclude = ['data_abert']
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
        exclude = ['saida_obj']
        widgets = {
            'observacao': forms.Textarea(attrs={
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super(EditarMaterialForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class MaterialTipoForm(forms.ModelForm):
    class Meta:
        model = MaterialTipo
        fields = '__all__'
        widgets = {
            'observacao': forms.Textarea(attrs={
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MaterialTipoForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class objMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialTipo
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(objMaterialForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class SaidaMaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialSaida
        fields = '__all__'
        exclude = ['data_saida']
    
    def __init__(self, *args, **kwargs):
        super(SaidaMaterialForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class FiltroForm(forms.Form):
    unidade = forms.ModelChoiceField(
        queryset=Unidade.objects.all(),
        label="Unidade",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.none(),
        label="Departamento",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    divisao = forms.ModelChoiceField(
        queryset=Divisao.objects.none(),
        label="Divisão",
        required=False,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    n_processo = forms.CharField(
        max_length=40,
        label="Número do processo(SEI)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        unidade_id = self.data.get('unidade')
        departamento_id = self.data.get('departamento')

        if unidade_id:
            self.fields['departamento'].queryset = Departamento.objects.filter(unidade_id=unidade_id)
        if departamento_id:
            self.fields['divisao'].queryset = Divisao.objects.filter(departamento_id=departamento_id)

    def clean_n_processo(self):
        n_processo = self.cleaned_data.get('n_processo')
        if not n_processo:
            raise forms.ValidationError("O número do processo é obrigatório.")
        return n_processo

class ProcessoForm(forms.Form):
    class Meta:
        model = 'MaterialSaida'
        fields = 'n_processo'

    def __init__(self, *args, **kwargs):
        super(ProcessoForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'






