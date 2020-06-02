from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm
from .forms import ProfileForm
from .models import Profile


# login
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("myBlog:article_list")
            else:
                return HttpResponse("Please enter the correct username and password for a staff account.")
        else:
            return HttpResponse("Please enter the correct username and password for a staff account.")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("Please use GET or POST")


# Logout
def user_logout(request):
    logout(request)
    return redirect("myBlog:article_list")


# register
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("myBlog:article_list")
        else:
            return HttpResponse("Something goes wrong! Please back and rewrite it.")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("you don't have authentic to modify data!")

        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            profile.email = profile_cd['email']
            profile.nationality = profile_cd['nationality']
            profile.profession = profile_cd['profession']
            profile.location = profile_cd['location']
            profile.real_name = profile_cd['real_name']
            profile.english_level = profile_cd['english_level']
            profile.skill1 = profile_cd['skill1']
            profile.skill2 = profile_cd['skill2']
            profile.skill3 = profile_cd['skill3']
            profile.skill4 = profile_cd['skill4']
            profile.skill5 = profile_cd['skill5']
            # 如果 request.FILES 存在文件，则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            # 带参数的 redirect()
            return redirect('myBlog:article_list')
        else:
            return HttpResponse("Something goes wrong! Please back and rewrite it.")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("Please use GET or POST")


# View Profile
@login_required(login_url='/userprofile/login/')
def profile_view(request, id):
    user = User.objects.get(id=id)

    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    context = {'profile': profile, 'user': user}
    return render(request, 'userprofile/profile.html', context)


# Contact page
def contact(request):
    return render(request, 'contact.html')
