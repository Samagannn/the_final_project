from django import forms


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

