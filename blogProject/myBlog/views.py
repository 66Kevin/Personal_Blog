from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ArticlePostForm, CommentForm
from .models import *
import markdown


def index(request):
    return HttpResponse("Welcome to my Blog!")


def article_list(request):
    template = 'article/list.html'
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')

    article_list = Article.objects.all()
    article_all = Article.objects.all()

    if search:
        article_list = article_list.filter(Q(title__icontains=search) | Q(content__icontains=search))
    else:
        search = ''

    if column is not None:
        article_list = article_list.filter(column__title__contains=column)

    if order:
        article_list = Article.objects.all().order_by('-total_views')

    # OrderByViews（first 3)
    article_view_list = Article.objects.all().order_by('-total_views')[:3]
    # Paginator
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles,
        'articles_all': article_all,
        'order': order,
        'search': search,
        'column': column,
        'articles_view_list': article_view_list
    }
    return render(request, template, context)


# Article detail page
def article_detail(request, id):
    template = 'article/detail.html'
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=id)

    article.total_views += 1
    article.save(update_fields=['total_views'])

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.content = md.convert(article.content)

    context = {'article': article, 'toc': md.toc, 'comments': comments}

    return render(request, template, context)


# safe delete article
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect("myBlog:article_list")
    else:
        return HttpResponse("ONlY support POST")

@login_required(login_url='/userprofile/login/')
def article_create(request):
    template = 'article/create.html'
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = Category.objects.get(id=request.POST['column'])
            new_article.save()
            return redirect('myBlog:article_list')
        else:
            return HttpResponse("something wrong")
    else:
        article_post_form = ArticlePostForm()
        columns = Category.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request, template, context)


# Update post
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    redirectAddr = "myBlog:article_detail"
    template = 'article/update.html'
    article = Article.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("Sorry,you don't have authorised to modify this post.")

    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.content = request.POST['content']
            if request.POST['column'] != 'none':
                article.column = Category.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            return redirect(redirectAddr, id=id)
        else:
            return HttpResponse("Something went wrong :-(")
    else:
        # create a new form
        article_post_form = ArticlePostForm()
        columns = Category.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }
        return render(request, template, context)


# # About me
# def resume(request):
#     return render(request, 'resume.html')


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
            return HttpResponse("Something went wrong :-(")
    # 处理错误请求
    else:
        return HttpResponse("ONLY support POST。")
