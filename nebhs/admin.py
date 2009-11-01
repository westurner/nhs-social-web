from django.contrib import admin
from nebhs.models import Animal
from gaegene.image.models import GeneImage

#class FileInline(admin.TabularInline):
#    model = File

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_url',)
admin.site.register(GeneImage, PhotoAdmin)


class AnimalAdmin(admin.ModelAdmin):
    #inlines = (FileInline,)
    list_display = ('code','category', 'name', 'breed',)

admin.site.register(Animal, AnimalAdmin)
