from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторіть пароль')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p1 != p2:
            raise forms.ValidationError('Паролі не співпадають')
        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        from .models import Profile
        model = Profile
        fields = ('display_name', 'avatar')
