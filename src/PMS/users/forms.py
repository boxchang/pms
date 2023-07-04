from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import *
 # extend Django's built-in UserCreationForm and UserChangeForm to
 # remove the username field (and optionally add any others that are
 # required)

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)


    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = '__all__'

# ======================================================
 # Forms for users themselves edit their profiles
 # ======================================================
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, HTML, Field
from .models import CustomUser

class CurrentCustomUserForm(forms.ModelForm):
    user_type = forms.ModelChoiceField(label="類別", queryset=UserType.objects.all(), widget=forms.Select(
        attrs={'class': "form-select"}))
    is_active = forms.BooleanField(label="是否啟用", initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    password1 = forms.CharField(label="密碼", required=False, widget=forms.PasswordInput(attrs={'placeholder': '請輸入登入密碼'}))
    password2 = forms.CharField(label="確認密碼", required=False, widget=forms.PasswordInput(attrs={'placeholder': '請再次輸入登入密碼'}))
    emp_no = forms.CharField(label="工號", widget=forms.TextInput(attrs={'placeholder': '工號'}))
    username = forms.CharField(label="姓名")

    class Meta:
        model = CustomUser
        fields = ('emp_no', 'username', 'last_name', 'first_name', 'user_type', 'email',
                  'is_active', 'password1', 'password2', 'username')

    def __init__(self, *args, submit_title="儲存編輯", **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('user_type', css_class="col-sm-4"),
                Div('emp_no', css_class="col-sm-4"),
                Div('username', css_class="col-sm-4"),
                css_class='row'
            ),
            Div(
                Div('username', css_class="col-sm-3"),
                Div('last_name', css_class="col-sm-3"),
                Div('first_name', css_class="col-sm-3"),
                Div(
                    HTML('<div class="form-switch">'),
                    Field('is_active'),
                    HTML('</div>'), css_class='col-md-3 text-center'),
                css_class='row'
            ),
            Div(
                Div('email', css_class="col-sm-12"),
                css_class='row'
            ),
            Div(

                Div('password1', css_class="col-sm-4"),
                Div('password2', css_class="col-sm-4"),
                css_class='row'
            ),
        )

    def clean(self):
        cleaned_data = super(CurrentCustomUserForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "密碼與確認密碼不一致"
            )


class UserInfoForm(forms.ModelForm):
    emp_no = forms.CharField(label="登入帳號", widget=forms.HiddenInput())
    password0 = forms.CharField(label="舊密碼", required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': '請輸入登入密碼'}))
    password1 = forms.CharField(label="新密碼", required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': '請輸入登入密碼'}))
    password2 = forms.CharField(label="確認密碼", required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': '請再次輸入登入密碼'}))

    class Meta:
        model = CustomUser
        fields = ('emp_no', 'email', 'password0', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Fieldset('基本資料',
                 Div(
                     Div('emp_no', css_class="col-sm-4"),
                     css_class='row'
                 ),
                 Div(
                     Div('email', css_class="col-sm-4"),
                     css_class='row'
                 ),
            ),
            HTML('<hr>'),
            Fieldset('密碼變更',
                Div(
                    Div('password0', css_class="col-sm-4"),
                    css_class='row p-3'
                ),
                Div(
                    Div('password1', css_class="col-sm-4"),
                    Div('password2', css_class="col-sm-4"),
                    css_class='row p-3'
                ),
            ),
            HTML('<hr>'),
        )

    def clean(self):
        cleaned_data = super(UserInfoForm, self).clean()
        emp_no = cleaned_data.get("emp_no")
        current_password = cleaned_data.get("password0")
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "密碼與確認密碼不一致"
            )

        if current_password and not authenticate(username=emp_no, password=current_password):
            raise forms.ValidationError(
                "舊密碼不正確"
            )
