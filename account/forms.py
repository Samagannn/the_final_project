from django import forms
from election.models import Candidate


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')


class CandidateInfoForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['election', 'party', 'bio']
