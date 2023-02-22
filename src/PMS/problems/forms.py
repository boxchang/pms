from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from problems.models import Problem, Problem_reply, ProblemType
from projects.models import Project
from django.utils.translation import gettext_lazy as _


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('problem_type', 'title', 'desc')

    problem_type = forms.ModelChoiceField(required=False, label="問題類型", queryset=ProblemType.objects.all(), initial=1)
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_('desc'), widget=CKEditorUploadingWidget())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['project'].widget.attrs['hidden'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        # if submit_title:
        #     self.helper.add_input(Submit('submit', submit_title))
        self.helper.layout = Layout(
            Div(
                Div('problem_type', css_class='col-md-3'),
                Div('title', css_class='col-md-9'),
                css_class='row'),
            Div('desc'),
        )


class ProblemReplyForm(forms.ModelForm):
    class Meta:
        model = Problem_reply
        fields = ('comment', )

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    comment = forms.CharField(
        required=True, label='', widget=CKEditorUploadingWidget())
