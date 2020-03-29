from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
)


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'login username',
            'placeholder': 'Enter username...',
            'style': 'border-radius: 4px;',
        }
    ), )

    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'login password',
            'placeholder': 'Enter password...',
            'style': 'border-radius: 4px;',
        }
    ), )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    'Oh! I can\'t find that user - create user first!')
            elif not user.check_password(password):
                raise forms.ValidationError(
                    'Oh! That password is incorrect - try again!')
            elif not user.is_active:
                raise forms.ValidationError(
                    'Oh! That user is not active in the database!')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'signup username',
            'placeholder': 'Enter username...',
            'style': 'border-radius: 4px;',
        }
    ), )
    first_name = forms.CharField(label='', required=False, widget=forms.TextInput(
        attrs={
            'class': 'signup firstname',
            'placeholder': 'Enter first name...',
            'style': 'border-radius: 4px;',
        }
    ), )
    last_name = forms.CharField(label='', required=False, widget=forms.TextInput(
        attrs={
            'class': 'signup lastname',
            'placeholder': 'Enter last name...',
            'style': 'border-radius: 4px;',
        }
    ), )
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={
            'class': 'signup email',
            'placeholder': 'Enter email...',
            'style': 'border-radius: 4px;',
        }
    ),)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'signup pass1',
            'placeholder': 'Enter password...',
            'style': 'border-radius: 4px;',
        }
    ), )
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'signup pass2',
            'placeholder': 'Confirm password...',
            'style': 'border-radius: 4px;',
        }
    ), )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        if password1 != password2:
            raise forms.ValidationError("Password must match")
        return super(UserRegisterForm, self).clean(*args, **kwargs)
