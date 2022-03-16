from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


# Sign Up Form
class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=True)
    # last_name = forms.CharField(max_length=30, required=True)
    # # list=['first_name','last_name']
    # # username = ' '.join(list)
    # # username=forms.CharField(username,required=True)
    # email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'firstname',
            'lastname',
            'email',
            'password1',
            'password2',
        ]


# Profile Form
class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
