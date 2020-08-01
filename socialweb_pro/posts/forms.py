from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['id'] = 'info7'
    class Meta():
        model=Post
        fields = ('message',)
