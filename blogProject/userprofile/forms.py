from django import forms
from django.contrib.auth.models import User
from .models import Profile, ResumePersonalInfo, ResumeEducation, ResumeJob, ResumeReserach, ResumeSkillset


# LoginForm
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required"}),
                               max_length=50)
    password = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Password", "required": "required"}),
                               max_length=20)


# RegisterForm
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Password", "required": "required"}),
                               max_length=20)
    password2 = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Password", "required": "required"}),
                                max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email')

    # check if the 2 passwords are equal
    def clean_password2(self):
        data = self.cleaned_data
        # 从POST中取值用get()
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")


# Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio', 'email', 'nationality', 'real_name','profession', 'english_level', 'location', 'skill1', 'skill2', 'skill3', 'skill4', 'skill5')


# ResumePersonalInfoForm
class ResumePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = ResumePersonalInfo
        fields = ('phone', 'avatar', 'address', 'real_name', 'website', 'email', 'current_status', 'linkedin', 'github')


# ResumePersonalInfoForm
class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        fields = ('name', 'programme', 'start_date', 'completion_date', 'summary', 'is_current')


# ResumeJob
class ResumeJobForm(forms.ModelForm):
    class Meta:
        model = ResumeJob
        fields = ('company', 'location','title','description','start_date','completion_date','is_current','is_public')


# ResumeReserach
class ResumeReserachForm(forms.ModelForm):
    class Meta:
        model = ResumeReserach
        fields = ('name','location','start_date','completion_date','summary')


# ResumeSkillset
class ResumeSkillsetForm(forms.ModelForm):
    class Meta:
        model = ResumeSkillset
        fields = ('name',)