from django import forms
from .models import ProvisaoGasto, ProjetoIniciativa

class ProvisaoGastoForm(forms.ModelForm):
    class Meta:
        model = ProvisaoGasto
        fields = [
            'id_projeto',
            'projeto',
            'iniciativa',
            'descricao',
            'provisao',
            'sap',        
            'fornecedor',
        ]
        widgets = {
            'id_projeto': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'projeto': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'iniciativa': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'sap': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'provisao': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
        }


class ProjetoIniciativaForm(forms.ModelForm):
    class Meta:
        model = ProjetoIniciativa
        fields = [
            'comite',
            'e_car',
            'projetos_para_extracao',
            'iniciativa',
            'descricao',
            'planta',
            'ano_aprovacao',
            'bdgt',
            'status',
            'orcamento',
            'disposto_sem_imposto',
            'valor_total_pedidos_emitidos',
            'valor_total_pedidos_pagos',
            'provisao',
        ]
        widgets = {
            'comite': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'e_car': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'projetos_para_extracao': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'iniciativa': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'planta': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'ano_aprovacao': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'bdgt': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'status': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'orcamento': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'disposto_sem_imposto': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'valor_total_pedidos_emitidos': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'valor_total_pedidos_pagos': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'provisao': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }
