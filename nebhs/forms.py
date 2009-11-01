# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _, ugettext as __
from nebhs.models import Animal
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField

class AnimalForm(forms.ModelForm):
    code = forms.CharField()
    name = forms.CharField()
    spay_or_neuter = forms.CharField() # TODO: coalesce to boolean

    class Meta:
        model = Animal
        #exclude = UserTraits.properties().keys()
