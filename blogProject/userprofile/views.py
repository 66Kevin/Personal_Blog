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
    template = 'userprofile/login.html'
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("myBlog:article_list")
            else:
                return HttpResponse("Please enter the correct username and password for a staff account.")
        else:
            return HttpResponse("Please enter the correct username and password for a staff account.")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")


# Logout
def user_logout(request):
    redirectAddr = "myBlog:article_list"
    logout(request)
    return redirect(redirectAddr)


# register
def user_register(request):
    redirectAddr = "myBlog:article_list"
    template = 'userprofile/register.html'
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, template, context)
    else:
        return HttpResponse("ONLY accept POST or GET")


# edit profile
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    redirectAddr = 'myBlog:article_list'
    template = 'userprofile/edit.html'

    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("you don't have authentic to modify data!")

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
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
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")


# View Profile
@login_required(login_url='/userprofile/login/')
def profile_view(request, id):
    template = 'userprofile/profile.html'
    user = User.objects.get(id=id)

    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    context = {'profile': profile, 'user': user}
    return render(request, template, context)


# Contact page
def contact(request):
    return render(request, 'contact.html')
