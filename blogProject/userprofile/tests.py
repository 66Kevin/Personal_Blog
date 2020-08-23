from datetime import datetime
from django.test import TestCase
from django.urls import resolve
from .models import ResumePersonalInfo, ResumeEducation, ResumeJob, ResumeReserach
from .views import show_resume, resumePersonalInfo_edit, showResumeEducation, showResumeJob, showResumeResearch, \
    resumeEducation_add, resumeJob_add, resumeResearch_add

get_now = datetime.now().strftime('%Y-%m-%d')


class ResumePageTests(TestCase):
    def setUp(self):
        ResumePersonalInfo.objects.create(user_id=1,real_name='Yueyi Wang',
                                          phone='7873709453', current_status='Student')

        ResumeEducation.objects.create(name='University of Birmingham', programme='Bsc Computer Science',
                                       start_date = get_now, completion_date = get_now, is_current = False)

        ResumeJob.objects.create(company='tencent',location='Beijing',title='AI',
                                 start_date=get_now,completion_date=get_now,
                                 description='Artificial intelligence engineer',is_current=False)

        ResumeReserach.objects.create(name='Face Mask Detection',location='Birmingham',
                                      start_date=get_now,completion_date=get_now, summary='testtesttest', )

    def test_url_resolves_to_resume_page_view(self):
        found = resolve('/userprofile/resume/')
        self.assertEqual(found.url_name, 'resume')
        self.assertEqual(found.func, show_resume)

    def test_resume_page(self):
        url = '/userprofile/resume/'
        template ='resume.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,template)

    def test_root_url_resolves_to_editResumePersonalInfo_page_view(self):
        found = resolve('/userprofile/editResumePersonalInfo/')
        self.assertEqual(found.url_name, 'editResumePersonalInfo')
        self.assertEqual(found.func, resumePersonalInfo_edit)

    def test_editResumePersonalInfo_POST_action(self):
        url = '/userprofile/editResumePersonalInfo/'
        data ={'real_name':'Yueyi Wang',
               'phone':'7873709453',
               'current_status':'Student',
               'address':'the metalworks',
               'website':'adfafsfaf.com',
               'email':'124543@qq.com'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_showResumeEducation_page_view(self):
        found = resolve('/userprofile/showResumeEducation/')
        self.assertEqual(found.url_name, 'showResumeEducation')
        self.assertEqual(found.func, showResumeEducation)

    def test_url_resolves_to_showResumeJob_page_view(self):
        found = resolve('/userprofile/showResumeJob/')
        self.assertEqual(found.url_name, 'showResumeJob')
        self.assertEqual(found.func, showResumeJob)

    def test_url_resolves_to_showResumeResearch_page_view(self):
        found = resolve('/userprofile/showResumeResearch/')
        self.assertEqual(found.url_name, 'showResumeResearch')
        self.assertEqual(found.func, showResumeResearch)

    def test_showResumeJob_GET_action(self):
        url = '/userprofile/showResumeEducation/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_showResumeEducation_GET_action(self):
        url = '/userprofile/showResumeEducation/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_showResumeResearch_GET_action(self):
        url = '/userprofile/showResumeResearch/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class ResumeEducationTests(TestCase):

    def setUp(self):
        ResumeEducation.objects.create(name='University of Birmingham',
                                       programme='Bsc Computer Science',
                                       start_date = get_now,
                                       completion_date = get_now,
                                       is_current = False)

    def test_ResumeEducation_models(self):
        name = ResumeEducation.objects.get(name="University of Birmingham")
        self.assertEqual(name.name, "University of Birmingham")
        self.assertEqual(name.programme, "Bsc Computer Science")
        self.assertFalse(name.is_current)

    def test_ResumeEducation_exist(self):
        self.assertEqual(ResumeEducation.objects.filter(name='University of Birmingham').count(), 1)

    def test_url_resolves_to_resumeEducationAdd_page_view(self):
        found = resolve('/userprofile/addResumeEducation/')
        self.assertEqual(found.url_name, 'resumeEducation_add')
        self.assertEqual(found.func, resumeEducation_add)

    def test_addResumeEducation_POST_action(self):
        url = '/userprofile/addResumeEducation/'
        data ={'name':'University of Birmingham',
               'programme':'Bsc Computer Science',
               'start_date' : get_now,
               'completion_date' : get_now,
               'is_current' : False}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, 200)


class ResumeJobTests(TestCase):

    def setUp(self):
        ResumeJob.objects.create(company='tencent',
                                location='Beijing',
                                title = 'AI',
                                start_date=get_now,
                                completion_date=get_now,
                                description = 'Artificial intelligence engineer',
                                is_current = False)

    def test_ResumeJob_models(self):
        company = ResumeJob.objects.get(company='tencent')
        self.assertEqual(company.company, "tencent")
        self.assertEqual(company.location, "Beijing")
        self.assertEqual(company.description,'Artificial intelligence engineer')
        self.assertFalse(company.is_current)

    def test_ResumeJob_exist(self):
        self.assertEqual(ResumeJob.objects.filter(company='tencent').count(), 1)

    def test_url_resolves_to_resumeJobAdd_page_view(self):
        found = resolve('/userprofile/addResumeJob/')
        self.assertEqual(found.url_name, 'resumeJob_add')
        self.assertEqual(found.func, resumeJob_add)

    def test_addResumeJob_POST_action(self):
        url = '/userprofile/addResumeJob/'
        data ={'company':'tencent',
               'location':'Beijing',
               'title' : 'AI',
               'description' : 'Artificial intelligence engineer',
               'is_current' : False}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class ResumeReserachTests(TestCase):

    def setUp(self):
        ResumeReserach.objects.create(name='Face Mask Detection',
                                      location='Birmingham',
                                      start_date=get_now,
                                      completion_date=get_now,
                                      summary = 'testtesttest',)

    def test_ResumeReserach_models(self):
        name = ResumeReserach.objects.get(name='Face Mask Detection')
        self.assertEqual(name.location, 'Birmingham')
        self.assertEqual(name.summary, 'testtesttest')

    def test_ResumeReserach_exist(self):
        self.assertEqual(ResumeReserach.objects.filter(name='Face Mask Detection').count(), 1)

    def test_url_resolves_to_resumeResearchAdd_page_view(self):
        found = resolve('/userprofile/addResumeResearch/')
        self.assertEqual(found.url_name, 'resumeResearch_add')
        self.assertEqual(found.func, resumeResearch_add)

    def test_addResumeResearch_POST_action(self):
        url = '/userprofile/addResumeResearch/'
        data ={'name':'Face Mask Detection',
               'location':'Birmingham',
                'summary' : 'testtesttest',}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, 200)