from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Jobseeker,Company

class JobseekerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_jobseeker = True
        user.email = self.cleaned_data.get('email')
        user.save()
        jobseeker = Jobseeker.objects.create(user=user)
        jobseeker.full_name = self.cleaned_data.get('full_name')
        jobseeker.save()
        return user
    


    
class JobseekerForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Jobseeker
        fields = ['full_name','cover_photo','phone_number', 'location', 'age', 'gender']

    def __init__(self, *args, **kwargs):
        super(JobseekerForm, self).__init__(*args, **kwargs)
        self.fields['skills'].choices = kwargs.get('skills_choices', [])








class CompanySignUpForm(UserCreationForm):
    company_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.is_staff = True
        user.save()
        company = Company.objects.create(user=user)
        company.company_name = self.cleaned_data.get('company_name')
        company.save()
        return user
    

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name','phone_number','designation']