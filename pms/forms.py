from django import forms
from pms.models import Student, Supervisor, SupervisorPreference, EligibleStudent
from django.contrib.auth.models import User
import re



class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "****************"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "****************"}))
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
             }
   
class StudentProfileForm(forms.ModelForm):

    class Meta:
        choice = {
                    ("Computer Engineering","Computer Engineering"),
                    ("Computer Science with Mathematics","Computer Science with Mathematics"),
                    ("Computer Science with Economics","Computer Science with Economics")
                    }
        model = Student
        fields = '__all__'
        widgets = {
            'image':forms.FileInput,
            'surname': forms.TextInput(attrs={'placeholder': 'Surname'}),
            'phone_no': forms.TextInput(attrs={'placeholder': '08060006000'}),
            
             }
        exclude = ('user', 'slug', 'created',)
        exclude = ('supervisor', 'user', 'slug', 'created', 'matricNo',)

    # def __init__(self, *args, **kwargs):
    #     super(StudentProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['option'].empty_label = '(-------Choose Your Option)'

class SupervisorProfileForm(forms.ModelForm):

    class Meta:
        model = Supervisor
        fields = '__all__'
        widgets = {
            'image':forms.FileInput,
            'surname': forms.TextInput(attrs={'placeholder': 'Surname'}),
            'phone_no': forms.TextInput(attrs={'placeholder': '08060006000'}),
             }
        exclude = ('user', 'slug', 'created',)


class SupervisorPreferenceForm(forms.ModelForm):

    class Meta:
        model = SupervisorPreference
        fields = ('student',)
        widgets = {
            'student': forms.Select(attrs={'class': "input-inline"})
             }
    
    def clean_student(self):
        try:
            SupervisorPreference.objects.get(student=self.cleaned_data['student'])
        except:
            return self.cleaned_data['student']
        raise forms.ValidationError("Matric Number Already Exist")

class EligibleStudentForm(forms.ModelForm):

    class Meta:
        model = EligibleStudent
        fields = ('name', 'matricNo')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'matricNo': forms.TextInput(attrs={'placeholder': 'Matric No without slash(/)'}),
             }
    
    def clean_matricNo(self):
        matricNo = self.cleaned_data['matricNo']
        matricNo = re.sub(r'\W+', '', matricNo)
        return matricNo


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Matric_No/Username'}),
            'password': forms.TextInput(attrs={'placeholder': 'Password'}),
             }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = " "
        self.fields["password"].label = " "

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "search User", 'class': "input-inline"}))

class UploadFileForm(forms.Form):
    sheet = forms.FileField()
