from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import html

class SubmitButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return '<input type="submit" name="%s" value="%s", >' % (html.escape(name), html.escape(value))


class SubmitButtonField(forms.Field):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs["widget"] = SubmitButtonWidget

        super(SubmitButtonField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value


class CommentForm(forms.Form):
    comment = forms.CharField(label='comment', widget = forms.Textarea)
    attachments = forms.FileField(required = False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

class ThreadForm(forms.Form):
    name = forms.CharField(label = 'thread name', max_length = 200)
    tags = forms.CharField(label = 'thread tags', widget = forms.TextInput(attrs = {'placeholder':'A comma separated list of tags', 'size': '50'}), required = False)

class ForumForm(forms.Form):
    name = forms.CharField(label = 'forum name', max_length = 200)

class VoteForm(forms.Form):
    upvote = SubmitButtonField(label = '', initial = u'Upvote')
    downvote = SubmitButtonField(label = '', initial = u'Downvote')

    def __init(self, *args, **kwargs):
        self.upvote.initial = self.downvote.initial = kwargs['thread']