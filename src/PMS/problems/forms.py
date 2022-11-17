from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from problems.models import Problem, Problem_reply
from projects.models import Project
from django.utils.translation import gettext_lazy as _


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('project', 'title', 'desc')

    project = forms.ModelChoiceField(required=True, label=_(
        'project'), queryset=Project.objects.all(), widget=forms.HiddenInput())
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_(
        'desc'), widget=CKEditorWidget())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['project'].widget.attrs['hidden'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        # if submit_title:
        #     self.helper.add_input(Submit('submit', submit_title))
        self.helper.layout = Layout(
            Div('project'),
            Div('title'),
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
        required=True, label='', widget=CKEditorUploadingWidget(config_name='special'))
