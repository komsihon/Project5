from django.forms import ModelForm, TextInput
from .models import Question
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from django import forms
from django.forms import ModelForm
from faq.models import Question


class QueryForm(forms.Form):
    queried_question = forms.CharField(max_length=200)
    # class Meta:
    #     model = Question
    #     fields = ['text']

# def question (request):

