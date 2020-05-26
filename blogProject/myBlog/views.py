from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from .models import *
import markdown


def index(request):
    return HttpResponse("Welcome to my Blog!")


def article_list(request):
    # 取出所有博客文章
    articles = Article.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = Article.objects.get(id=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.content = md.convert(article.content)

    # 需要传递给模板的对象
    context = {'article': article,
               'toc': md.toc,}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect("myBlog:article_list")
    else:
        return HttpResponse("仅允许post请求")


def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)

            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()

            return redirect('myBlog:article_list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


# Update post
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = Article.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("Sorry,you don't have authorised to modify this post.")

    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("Something Wrong! Please re-write it.")
    else:
        # create a new form
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)


# About me
def about(request):
    return render(request, 'about.html')
