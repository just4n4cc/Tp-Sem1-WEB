from django import forms
from django.contrib.auth.models import User
from app.models import Question, Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            self.add_error(None, 'Passwords mismatch!')

        return cleaned_data


class SettingsForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

