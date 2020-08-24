from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, ResumePersonalInfo, ResumeEducation, ResumeJob, ResumeReserach, ResumeSkillset


# 定义一个行内 admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'


# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(ResumePersonalInfo)
class ResumePersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('real_name','phone','website','email')
    fieldsets = (
        (None, {
            'fields': ('user','real_name', 'phone', 'website', 'email', 'current_status','address', 'linkedin', 'github')
                }),)


@admin.register(ResumeEducation)
class ResumeEducationAdmin(admin.ModelAdmin):
    list_display = ('name','programme','start_date','completion_date')
    fieldsets = (
        (None, {
            'fields': ('name', 'programme', 'start_date', 'completion_date', 'summary', 'is_current')
                }),)


@admin.register(ResumeJob)
class ResumeJobAdmin(admin.ModelAdmin):
    list_display = ('company','location','title',)
    fieldsets = (
        (None, {
            'fields': ('company', 'location', 'title', 'start_date', 'completion_date', 'is_current')
                }),)


@admin.register(ResumeReserach)
class ResumeReserachAdmin(admin.ModelAdmin):
    list_display = ('name','location',)
    fieldsets = (
        (None, {
            'fields': ('name','location', 'start_date', 'completion_date', 'summary')
                }),)


@admin.register(ResumeSkillset)
class ResumeSkillsetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)
                }),)