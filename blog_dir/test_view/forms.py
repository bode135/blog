from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


# 引入表单类
from django import forms
# 引入文章模型
from .models import AuthorPost

# 写文章的表单类
class CreateAuthorForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = AuthorPost
        # 定义表单包含的字段
        # fields = ['__all__']
        fields = ['name']


