from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ArticlePostForm, CommentForm
from .models import *
import markdown


def index(request):
    return HttpResponse("Welcome to my Blog!")


def article_list(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    # articles = paginator.get_page(page)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = { 'articles': articles }
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):

    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=id)

    article.total_views += 1
    article.save(update_fields=['total_views'])

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

    context = {'article': article, 'toc': md.toc, 'comments': comments}

    return render(request, 'article/detail.html', context)


# safe delete article
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
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = Category.objects.get(id=request.POST['column'])
            new_article.save()
            return redirect('myBlog:article_list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = Category.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
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
            if request.POST['column'] != 'none':
                article.column = Category.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("myBlog:article_detail", id=id)
        else:
            return HttpResponse("Something Wrong! Please re-write it.")
    else:
        # create a new form
        article_post_form = ArticlePostForm()
        columns = Category.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }
        return render(request, 'article/update.html', context)


# About me
def about(request):
    return render(request, 'about.html')


# Comment
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("Something Wrong! Please re-write it.")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")