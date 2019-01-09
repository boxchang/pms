from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
from crispy_forms.layout import Submit, Layout, Div
from .models import CustomUser

class CurrentCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name',
                  'mobile_number', 'email')
    def __init__(self, *args, submit_title="儲存編輯", **kwargs):
        super().__init__(*args, **kwargs)

        my_field_text= [
            ('email', '電子郵件', '電子郵件將會作為您往後登入時使用'),
            ('last_name', '姓', ''),
            ('first_name', '名', ''),
            ('mobile_number', '手機', '失蹤還能打電話關心一下'),
         ]
        for x in my_field_text:
            self.fields[x[0]].label=x[1]
            self.fields[x[0]].help_text=x[2]

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', submit_title))

        self.helper.layout = Layout(
            Div(
                Div('first_name', css_class="col-sm-6"),
                Div('last_name', css_class="col-sm-6"),
                css_class='row'
            ),
            Div('email'),
            Div('mobile_number'), )