# 引入表单类
from django import forms
# 引入文章模型
from .models import Article, Comment


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Article
        # 定义表单包含的字段
        fields = ('title', 'content', 'avatar')


class CommentForm(forms.ModelForm):
    # author = forms.CharField(widget=forms.TextInput(
    #     attrs={"id": "author", "class": "comment_input",
    #            "required": "required", "size": "25", "tabindex": "1"}),
    #     max_length=50, error_messages={"required": "USERNAME can't be empty"}
    # )
    # email = forms.EmailField(widget=forms.TextInput(
    #     attrs={"id": "email", "type": "email", "class": "comment_input",
    #            "required": "required", "size": "25", "tabindex": "2"}),
    #     max_length=50, error_messages={"required": "EMAIL can't be empty", })
    # url = forms.URLField(widget=forms.TextInput(
    #     attrs={"id": "url", "type": "url", "class": "comment_input",
    #            "size": "25", "tabindex": "3"}),
    #     max_length=100, required=False)
    # comment = forms.CharField(widget=forms.Textarea(
    #     attrs={"id": "comment", "class": "message_input",
    #            "required": "required", "cols": "25",
    #            "rows": "5", "tabindex": "4"}),
    #     error_messages={"required": "COMMENT can't be empty", })
    # article = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        # 指明数据模型来源
        model = Comment
        # 定义表单包含的字段
        fields = ('content',)
