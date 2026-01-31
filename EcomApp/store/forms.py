from django.forms import *

from . import models

class UserModelForm(ModelForm):
  class Meta:
    model=models.UserModelClass
    fields="__all__"
    widgets={
      'gender':RadioSelect(choices=[('Male','Male'),('Female','Female')])
    }