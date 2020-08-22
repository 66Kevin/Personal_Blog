from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm, ResumePersonalInfoForm, ResumeEducationForm, ResumeJobForm, \
    ResumeReserachForm
from .forms import ProfileForm
from .models import Profile, ResumePersonalInfo, ResumeEducation, ResumeSkillset, ResumeJob, ResumeReserach


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


# personal consume
def show_resume(request):
    template = 'resume.html'
    personal_info = ResumePersonalInfo.objects.all()[0]
    education = ResumeEducation.objects.all()
    job_list = ResumeJob.objects.all()
    skill_sets = ResumeSkillset.objects.all()
    research_list = ResumeReserach.objects.all()

    context = {'personal_info': personal_info,
               'job_list': job_list,
               'education': education,
               'skill_sets': skill_sets,
               'research_list': research_list,
               }

    return render(request, template , context)


# edit resume personal info part
def resumePersonalInfo_edit(request):
    redirectAddr = "userprofile:resume"
    template = 'userprofile/editResumePersonalInfo.html'

    if request.user.is_superuser:
        personal_info = ResumePersonalInfo.objects.all()[0]
    else:
        return HttpResponse("<font size=10px> You do not have permission to modify the data items<br>"
                            "only the SUPER USER can edit the resume<br>"
                            "Please login in !</font>")

    if request.method == 'POST':
        resumePersonalInfo_form = ResumePersonalInfoForm(request.POST, request.FILES)
        if resumePersonalInfo_form.is_valid():
            resumePersonalInfo_cd = resumePersonalInfo_form.cleaned_data
            personal_info.phone = resumePersonalInfo_cd['phone']
            personal_info.address = resumePersonalInfo_cd['address']
            personal_info.real_name = resumePersonalInfo_cd['real_name']
            personal_info.website = resumePersonalInfo_cd['website']
            personal_info.email = resumePersonalInfo_cd['email']
            personal_info.current_status = resumePersonalInfo_cd['current_status']
            personal_info.linkedin = resumePersonalInfo_cd['linkedin']
            personal_info.github = resumePersonalInfo_cd['github']
            if 'avatar' in request.FILES:
                personal_info.avatar = resumePersonalInfo_cd["avatar"]
            personal_info.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        resumePersonalInfo_form = ResumePersonalInfoForm()
        context = {'resumePersonalInfo_form': resumePersonalInfo_form,'resumePersonalInfo': ResumePersonalInfo.objects.all()[0]}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")

#########################################################################################################################


# show the resume detail in a new page to edit the data
def showResumeEducation(request):

    template = "userprofile/showResumeDetailtoEdit.html"

    # education_dict_list = [{'education1': xxxxx},{'education2': xxxxx},{'education3': xxxxx}]
    education_dict_list=[]
    for education in ResumeEducation.objects.all():
        education_dict = model_to_dict(education)
        education_dict_list.append(education_dict)

    educationFirstElementtoDictionary = model_to_dict(ResumeEducation.objects.all()[0])
    key_list = educationFirstElementtoDictionary.keys()

    context = {'dict_list': education_dict_list,
               'key_list': key_list,
               'add_address':'userprofile:resumeEducation_add',
               'edit_address':'userprofile:editResumeEducation'
               }

    return render(request, template, context)


def showResumeJob(request):

    template = "userprofile/showResumeDetailtoEdit.html"

    # job_dict_list = [{'education1': xxxxx},{'education2': xxxxx},{'education3': xxxxx}]
    job_dict_list=[]
    for job in ResumeJob.objects.all():
        job_dict = model_to_dict(job)
        job_dict_list.append(job_dict)

    jobFirstElementtoDictionary = model_to_dict(ResumeJob.objects.all()[0])
    key_list = jobFirstElementtoDictionary.keys()

    context = {'dict_list': job_dict_list,
               'key_list': key_list,
               'add_address': 'userprofile:resumeJob_add',
               'edit_address': 'userprofile:editResumeJob'
               }

    return render(request, template, context)


# show the resume detail in a new page to edit the data
def showResumeResearch(request):

    template = "userprofile/showResumeDetailtoEdit.html"

    # education_dict_list = [{'education1': xxxxx},{'education2': xxxxx},{'education3': xxxxx}]
    research_dict_list=[]
    for research in ResumeReserach.objects.all():
        research_dict = model_to_dict(research)
        research_dict_list.append(research_dict)

    researchFirstElementtoDictionary = model_to_dict(ResumeReserach.objects.all()[0])
    key_list = researchFirstElementtoDictionary.keys()

    context = {'dict_list': research_dict_list,
               'key_list': key_list,
               'add_address': 'userprofile:resumeResearch_add',
               'edit_address': 'userprofile:editResumeResearch',
               }

    return render(request, template, context)

#########################################################################################################################


# edit resume job part
def resumeJob_edit(request,id):
    redirectAddr = "userprofile:resume"
    template = 'userprofile/editResume.html'

    if request.user.is_superuser:
        job = ResumeJob.objects.get(id=id)
    else:
        return HttpResponse("<font size=10px> You do not have permission to modify the data items<br>"
                            "only the SUPER USER can edit the resume<br>"
                            "Please login in !</font>")

    if request.method == 'POST':
        job_form = ResumeJobForm(request.POST, request.FILES)
        if job_form.is_valid():
            job_cd = job_form.cleaned_data
            job.company = job_cd['company']
            job.location = job_cd['location']
            job.title = job_cd['title']
            job.description = job_cd['description']
            job.start_date = job_cd['start_date']
            job.completion_date = job_cd['completion_date']
            job.is_current = job_cd['is_current']
            job.is_public = job_cd['is_public']
            job.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        job_form = ResumeJobForm()
        job_identiy_dict = model_to_dict(ResumeJob.objects.get(id=id))
        context = {'job_form': job_form, 'identiy_dict': job_identiy_dict, 'whoWillBeDeleted': 'userprofile:resumeJob_delete'}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")


# edit resume education part
def resumeEducation_edit(request, id):
    redirectAddr = "userprofile:resume"
    template = 'userprofile/editResume.html'

    if request.user.is_superuser:
        education = ResumeEducation.objects.get(id=id)
    else:
        return HttpResponse("<font size=10px> You do not have permission to modify the data items<br>"
                            "only the SUPER USER can edit the resume<br>"
                            "Please login in !</font>")

    if request.method == 'POST':
        education_form = ResumeEducationForm(request.POST, request.FILES)
        if education_form.is_valid():
            education_cd = education_form.cleaned_data
            education.name = education_cd['name']
            education.programme = education_cd['programme']
            education.start_date = education_cd['start_date']
            education.completion_date = education_cd['completion_date']
            education.summary = education_cd['summary']
            education.is_current = education_cd['is_current']
            education.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        education_form = ResumeEducationForm()
        education_identiy_dict = model_to_dict(ResumeEducation.objects.get(id=id))
        context = {'education_form': education_form,
                   'identiy_dict': education_identiy_dict,
                   'whoWillBeDeleted': 'userprofile:resumeEducation_delete'
                   }
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")


# edit resume research part
def resumeReseach_edit(request, id):
    redirectAddr = "userprofile:resume"
    template = 'userprofile/editResume.html'

    if request.user.is_superuser:
        research = ResumeReserach.objects.get(id=id)
    else:
        return HttpResponse("<font size=10px> You do not have permission to modify the data items<br>"
                            "only the SUPER USER can edit the resume<br>"
                            "Please login in !</font>")

    if request.method == 'POST':
        research_form = ResumeReserachForm(request.POST, request.FILES)
        if research_form.is_valid():
            research_cd = research_form.cleaned_data
            research.name = research_cd['name']
            research.location = research_cd['location']
            research.start_date = research_cd['start_date']
            research.completion_date = research_cd['completion_date']
            research.summary = research_cd['summary']
            research.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        research_form = ResumeReserachForm()
        research_identiy_dict = model_to_dict(ResumeReserach.objects.get(id=id))
        context = {'research_form': research_form,
                   'identiy_dict': research_identiy_dict,
                   'whoWillBeDeleted': 'userprofile:resumeResearch_delete'}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")

#########################################################################################################################


def resumeEducation_delete(request, id):
    if request.method == 'POST':
        edu = ResumeEducation.objects.get(id=id)
        edu.delete()
        return redirect("userprofile:resume")
    else:
        return HttpResponse("ONlY support POST")


def resumeJob_delete(request, id):
    if request.method == 'POST':
        job = ResumeJob.objects.get(id=id)
        job.delete()
        return redirect("userprofile:resume")
    else:
        return HttpResponse("ONlY support POST")


def resumeResearch_delete(request, id):
    if request.method == 'POST':
        research = ResumeReserach.objects.get(id=id)
        research.delete()
        return redirect("userprofile:resume")
    else:
        return HttpResponse("ONlY support POST")

#########################################################################################################################


def resumeEducation_add(request):
    redirectAddr = "userprofile:resume"
    template = 'userprofile/addResumeItem.html'

    if request.method == 'POST':
        add_education_form = ResumeEducationForm(request.POST, request.FILES)
        if add_education_form.is_valid():
            new_education = add_education_form.save(commit=False)
            new_education.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        add_education_form = ResumeEducationForm()
        educationFirstElementtoDictionary = model_to_dict(ResumeEducation.objects.get(id=1))
        context = {'add_form': add_education_form, "identiy_dict": educationFirstElementtoDictionary,}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")


def resumeJob_add(request):
    redirectAddr = "userprofile:resume"
    template = 'userprofile/addResumeItem.html'

    if request.method == 'POST':
        add_job_form = ResumeJobForm(request.POST, request.FILES)
        if add_job_form.is_valid():
            new_job = add_job_form.save(commit=False)
            new_job.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        add_job_form = ResumeJobForm()
        jobFirstElementtoDictionary = model_to_dict(ResumeJob.objects.get(id=1))
        context = {'add_form': add_job_form, "identiy_dict": jobFirstElementtoDictionary,}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")


def resumeResearch_add(request):
    redirectAddr = "userprofile:resume"
    template = 'userprofile/addResumeItem.html'

    if request.method == 'POST':
        add_research_form = ResumeReserachForm(request.POST, request.FILES)
        if add_research_form.is_valid():
            new_research = add_research_form.save(commit=False)
            new_research.save()
            return redirect(redirectAddr)
        else:
            return HttpResponse("Something went wrong :-(")
    elif request.method == 'GET':
        add_research_form = ResumeReserachForm()
        researchFirstElementtoDictionary = model_to_dict(ResumeReserach.objects.get(id=1))
        context = {'add_form': add_research_form, "identiy_dict": researchFirstElementtoDictionary,}
        return render(request, template, context)
    else:
        return HttpResponse("Please use GET or POST")

########################################################################################################################


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
            return HttpResponse("you don't have authority to modify data!")

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
