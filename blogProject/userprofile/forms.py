# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required"}),
                               max_length=50)
    password = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Password", "required": "required"}),
                               max_length=20)


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
