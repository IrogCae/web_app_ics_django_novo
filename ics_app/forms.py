from django import forms
from .models import ProvisaoGasto

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
            'id_projeto': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'projeto':    forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'iniciativa': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'descricao':  forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'sap':        forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'fornecedor': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'provisao':   forms.NumberInput(attrs={'class':'form-control form-control-sm', 'step':'0.01'}),
          
        }