from django.contrib import admin
from misdir.models import *

class DegreeAdminInline(admin.TabularInline):
    model = Degree
    fields = ('name','degree_type','institution','status')
    fk_name = 'institution'

class DegreeAdmin(admin.ModelAdmin):
    model = Degree
    list_display = ('degree_type','name','institution')
    list_filter = ('degree_type',)

class StudentChapterAdmin(admin.ModelAdmin):
    list_display = ('name','institution','city','state','country','aissc_member','status')
    list_filter = ('aissc_member','status')

class InstitutionAdmin(admin.ModelAdmin):
    inlines = (DegreeAdminInline, )
    list_display = ('name','city','state')
    pass
    

class BusinessAdmin(admin.ModelAdmin):
    # TODO: BusinessLocations Inline
    list_display = ('name','city','state','aissc_sponsor','status')
    list_filter = ('aissc_sponsor','status')
    pass


admin.site.register(StudentChapter, StudentChapterAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Degree, DegreeAdmin)
