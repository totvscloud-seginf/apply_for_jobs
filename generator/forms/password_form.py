from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from generator.models import Password


class PasswordForm(forms.ModelForm):
    """
    Classe para renderização e validação dos dados oriundos do Model Password.
    """
    class Meta:
        model = Password
        fields = ['value', 'expiration_date', 'maximum_views']
        widgets = {
            'value': forms.HiddenInput(),
            'expiration_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            # Renderiza o formulário com um número mínimo de visualizacoes maior ou igual a 1 impedindo erro humano na
            # hora de gerar um link de senha que não poderá ser visualizo nem ao menos uma vez.
            'maximum_views': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }

    def clean_expiration_date(self):
        """
        Faz a validacao para verificar se a data obtida no formulario esta no passado.
        """
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date < date.today():
            raise ValidationError(f'Não é possível cadastrar uma data de expiração no passado.')
        else:
            return expiration_date
