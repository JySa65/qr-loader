from django import forms
from app.models import User, TokenQr


class DateInput(forms.DateInput):
    input_type = 'date'


class TokenQrForm(forms.ModelForm):

    class Meta:
        model = TokenQr
        fields = '__all__'


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('token',)
        widgets = {
            'birthday': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
        self.fields['address'].widget.attrs.update(
            {'rows': '2'})
