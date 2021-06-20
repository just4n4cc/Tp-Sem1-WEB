from django import forms
from django.contrib.postgres.forms import SplitArrayField
from django.contrib.auth.models import User
from app.models import Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        if not User.objects.filter(username=cleaned_data['username']).exists():
            self.add_error('username', 'Wrong username!')
        else:
            user = User.objects.get(username=cleaned_data['username'])
            if not user.check_password(cleaned_data['password']):
                self.add_error('password', 'Wrong password!')

        return cleaned_data


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
    avatar = forms.ImageField(required=False)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    tags = SplitArrayField(forms.CharField(max_length=50), size=5, remove_trailing_nulls=True, required=False)


class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea())
