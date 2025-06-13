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
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3,
                'placeholder': 'Descrição do material...',
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
            'descricao_contr': forms.Textarea(attrs={
                'rows': 4,
            }),
            'data_abert': forms.DateInput(attrs={
                'type': 'date',
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

    def __init__(self, *args, **kwargs):
        super(AddUnidadeForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class AddDepartForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddDepartForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control form-control-sm'

class AddDivisaoForm(forms.ModelForm):
    class Meta:
        model = Divisao
        fields = '__all__'
        widgets = {
            'departamento': forms.Select(attrs={
                'class': 'form-select form-select-sm',
                'style': 'max-height: 200px; overflow-y: auto; size: 5;',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # If it's a select, keep 'form-select' and add 'form-control-sm'
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select form-control-sm'
                field.widget.attrs['style'] = 'max-height: 200px; overflow-y: auto;'
            else:
                field.widget.attrs['class'] = 'form-control form-control-sm'

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
        self.fields['unidade'].widget.attrs.update({'class': 'form-control form-control-sm form-select'})
        self.fields['departamento'].widget.attrs.update({'class': 'form-control form-control-sm form-select'})
        self.fields['divisao_field'].widget.attrs.update({'class': 'form-control form-control-sm form-select'})

class FiltroForm(forms.Form):
    unidade = forms.ModelChoiceField(
        queryset=Unidade.objects.all(),
        label="Unidade",
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.none(),
        label="Departamento",
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )
    divisao = forms.ModelChoiceField(
        queryset=Divisao.objects.none(),
        label="Divisão",
        required=False,  
        widget=forms.Select(attrs={'class': 'form-control form-select'})
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

class BuscarItemForm(forms.Form):
    item = forms.CharField(max_length=80, required=True)

class getRelatorioForm(forms.Form):
    get_data = forms.CharField(max_length=80, required=True)





