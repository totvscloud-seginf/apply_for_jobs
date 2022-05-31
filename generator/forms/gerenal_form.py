from django import forms


class ExclusionForm(forms.Form):
    """
    Classe para renderização de formulário de confirmação para exclusão de ítens nos templates.
    """
    confirmation = forms.BooleanField(label='', required=True)
