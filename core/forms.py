from django import forms
from django.core.validators import RegexValidator
from .models import Survey, SurveyOption

class UserRegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'required': True
        }),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message='Name should only contain letters and spaces.'
            )
        ]
    )
    
    mobile_number = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 10-digit mobile number',
            'pattern': '[0-9]{10}',
            'required': True
        }),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Please enter a valid 10-digit mobile number.'
            )
        ]
    )

class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit OTP',
            'pattern': '[0-9]{6}',
            'required': True,
            'autocomplete': 'off'
        }),
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Please enter a valid 6-digit OTP.'
            )
        ]
    )

class SurveyCreationForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter survey title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter survey description',
                'rows': 4,
                'required': True
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }

class SurveyOptionForm(forms.ModelForm):
    class Meta:
        model = SurveyOption
        fields = ['option_text']
        widgets = {
            'option_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter option text',
                'required': True
            })
        }

class VotingForm(forms.Form):
    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_option'] = forms.ChoiceField(
            choices=[(option.id, option.option_text) for option in survey.options.all()],
            widget=forms.RadioSelect(attrs={
                'class': 'form-check-input',
                'required': True
            })
        )

