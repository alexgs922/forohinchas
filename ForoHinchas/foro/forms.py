from django import forms

from foro.models import Jornada, Post


class JornadaForm(forms.ModelForm):

    class Meta:
        model = Jornada
        exclude = ['author']


class PostForm(forms.ModelForm):
    text = forms.CharField()

    text.widget.attrs['id'] = u'comment'
    text.widget.attrs['class'] = u'form-control'
    text.widget.attrs['rows'] = u'5'

    class Meta:
        model = Post
        fields = ['text']
