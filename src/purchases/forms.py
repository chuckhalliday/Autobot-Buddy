from django import forms
from .models import ChatLog

input_css_class = "form-control"

class QuestionForm(forms.ModelForm):
    class Meta:
        model = ChatLog
        fields = ['question']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update({'class': input_css_class})