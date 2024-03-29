from django import forms
from employee_management.models import Funcionario

class InsereFuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = [
            'nome',
            'sobrenome',
            'cpf',
            'remuneracao',
        ]