import imp

from django.conf import settings
from unittest.mock import sentinel
from django.shortcuts import redirect, render
from requests.models import Response
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect, request
from .markdownprocess import markdownprocess
from .models import *
from .forms import *
from .markdown import *
from .answer import *

import pyautogui

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

import requests
import random
import string
import json

from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import Question
from .tables import QuestionTable
import markdown
import re


def logout_request(request):
    logout(request)
    
    try:
        del request.session['username']
    except:
        return redirect('login')
    
    return render(request, "QuestionElab/index.html", {"message": "Log out."})
    


def signup_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return render(request, "QuestionElab/login.html", {"message": "Registration successful."})
        #else :
            #messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render (request=request, template_name="QuestionElab/signup.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                messages.info(request, f"You are now logged in as {username}.")
                
                return HttpResponseRedirect(reverse("index"))
            
            else:
                return render(request, "QuestionElab/login.html", {
                            "message": "Invalid username or password."
                        })
        else:
            return render(request, "QuestionElab/login.html", {
                            "message": "Invalid username or password."
                        })
    form = AuthenticationForm()
    return render(request=request, template_name="QuestionElab/login.html", context={"login_form":form})



def index(request, id = None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if 'send' in request.POST:
        Qname = request.POST['Qname']
        Qlanguage = request.POST['Qlanguage']
        
        Qcondition = request.POST.getlist('Qcondition')
        
        exactmacth = False
        ignorespace = False
        sensitive = False
        insensitive = False
        for x in range(len(Qcondition)):
            if Qcondition[x] == "exactmacth":
                exactmacth = True
            elif Qcondition[x] == "ignorespace":
                ignorespace = True
            elif Qcondition[x] == "sensitive":
                sensitive = True
            elif Qcondition[x] == "insensitive":
                insensitive = True
            
        source = request.POST['source']
        Qelement = request.POST['Qelement']
        
        valuemarkdown = mdprocessmarkdown(source)
        valuemarkdownbetween = mdprocessmarkdownbetween(source)
        valuemarkdownlast = mdprocessmarkdownlast(source)
        valueoutput = mdprocessoutput(source)
        valueinput = mdprocessinput(source)

        context = {
            "Qname": Qname,
            "Qlanguage" : Qlanguage,
            "exactmacth" : exactmacth,
            "ignorespace" : ignorespace,
            "sensitive" : sensitive,
            "insensitive" : insensitive,
            "Qelement" : Qelement,
            "source": source,
            "resultmarkdown": valuemarkdown,
            "resultmarkdownbetween": valuemarkdownbetween,
            "resultmarkdownlast" : valuemarkdownlast,
            "resultoutput": valueoutput,
            "resultinput": valueinput,
            
        }
        
        return render(request,"QuestionElab/index.html", context=context)
    
    
    if 'save' in request.POST:
        result_str = randStr(chars='abcdefghijklmnopqrstuvwxyz1234567890') 
        # result_str = randStr(chars='abcdefghijklmnopqrstuvwxyz1234567890') 
        username = request.session['username']
        Qlanguage = request.POST['Qlanguage']
        Qname = request.POST['Qname']
        Qcondition = request.POST.getlist('Qcondition')
        source = request.POST['source']
        Qelement = request.POST['Qelement']
        # valueoutput = mdprocessoutput(source)
        # valueinput = mdprocessinput(source)
        p2 = Question.objects.create(question_username=username, question_token=result_str, question_language=Qlanguage , question_name=Qname, question_condition=Qcondition, question_source=source , question_element=Qelement )
        p2.save()
        
      
        return redirect('manage')
        # return render(request,"QuestionElab/manage.html")


    
    context = {
            "source": "",
        }
    
    if id != None :
        obj = Question.objects.get(id = id)
        if obj == 'null' :
            
            return render(request,"QuestionElab/index.html", context=context)
        
        else :
            context = {
            "Qname": obj.question_name,
            "Qcondition": obj.question_condition,
            "Qlanguage" : obj.question_language,
            "source": obj.question_source,
            "Qelement": obj.question_element
        }
            return render(request,"QuestionElab/index.html", context=context)
    else:
        return render(request,"QuestionElab/index.html", context=context)

def randStr(chars = string.ascii_uppercase + string.digits, N=15):
    return ''.join(random.choice(chars) for _ in range(N))

# def manage(request):
#     # objQuestion = Question.objects.all()
#     table = QuestionTable(Question.objects.all())
#     table.paginate(page=request.GET.get("page", 1), per_page=25)
    
#     # allcourse = Course.objects.all()
    
#     return render(request,"QuestionElab/manage.html", {
#         "table": table,
        
#     })
    
def manage(request):
    # objQuestion = Question.objects.all()
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    username = request.session['username']
    table = Question.objects.filter(question_username = username)
    
    # allcourse = Course.objects.all()
    
    return render(request,"QuestionElab/manage.html", {
        "tables": table,
        
    })

def delete(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    obj = Question.objects.get(id = id)
    
    obj.delete()
    return redirect('manage')


def share(request, id):
    
    obj = Question.objects.get(question_token = id)
    valuemarkdown = mdprocessmarkdown(obj.question_source)
    valuemarkdownbetween = mdprocessmarkdownbetween(obj.question_source)
    valuemarkdownlast = mdprocessmarkdownlast(obj.question_source)
    valueoutput = mdprocessoutput(obj.question_source)
    valueinput = mdprocessinput(obj.question_source)
    
    if 'check' in request.POST:
        con = ""
        lang = ""
        elem = "[check-element]:#"
        obj = Question.objects.get(question_token = id)
        if len(valueinput) == 0:
            con += "[check-output]:#no-input"
        else :
            con += "[check-output]:#input"
            
        if obj.question_language == "python":
            lang = "[language]:#py"
        elif obj.question_language == "java":
            lang = "[language]:#java"
        elif obj.question_language == "c":
            lang = "[language]:#c"
            
        if "exactmacth" in obj.question_condition :
            con += "//exact-macth"
        if "ignorespace" in obj.question_condition :
            con += "//ignore-space"
        if "sensitive" in obj.question_condition :
            con += "//sensitive"
        if "insensitive" in obj.question_condition :
            con += "//insensitive"

        elem += obj.question_element
        answer = request.POST['answer']
        ans = Answer(lang, con, elem, valueinput.replace('<br>','\n'), valueoutput.replace('<br>','\n'), answer)
        messages.success(request, "Your answer has been checked successfully!")
        jsonstr1= json.dumps(ans.__dict__)
        
        context = {
            "ans": jsonstr1,
            
        }
        
        return render(request,"QuestionElab/check.html", context=context)

    if 'api' in request.POST:
        con = ""
        lang = ""
        elem = "[check-element]:#"
        obj = Question.objects.get(question_token = id)
        if len(valueinput) == 0:
            con = "[check-output]:#no-input"
        else :
            con = "[check-output]:#input"
            
        if obj.question_language == "python":
            lang = "[language]:#py"
        elif obj.question_language == "java":
            lang = "[language]:#java"
        elif obj.question_language == "c":
            lang = "[language]:#c"
            
        if "exactmacth" in obj.question_condition :
            con += "//exact-macth"
        if "ignorespace" in obj.question_condition :
            con += "//ignore-space"
        if "sensitive" in obj.question_condition :
            con += "//sensitive"
        if "insensitive" in obj.question_condition :
            con += "//insensitive"
        
        answer = request.POST['answer']
        elem += obj.question_element
        ans = Answer(lang, con, elem, valueinput.replace('<br>','\n'), valueoutput.replace('<br>','\n'), answer)
        
        text = lang +"\n" + "::startcode::\n" + answer +"\n"+ "::endcode::\n" + con +"\n" + "::start-input::\n" + valueinput.replace('<br>','\n')+"\n" + "::end-input::\n" + "::start-output::\n" + valueoutput.replace('<br>','\n')+"\n" + "::end-output::\n" + elem
        print("text" + text)
        
        url = "https://0f71-2405-9800-ba10-f053-5c90-3696-8000-8497.ap.ngrok.io/textapi"

        payload={'text': text}

        # files=[

        #     ('file',('file','','application/octet-strpyteam')),

        #     ('inputfile',('file','','application/octet-stream'))

        # ]

        # headers = {}

        response = requests.request("POST", url,  data=payload)
        # response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            print("success")
            print(response.text)
            messages.success(request, "Your answer has been sent successfully1")
            # messages.info(request, 'Success')
            return HttpResponseRedirect('/share/'+id)
        else:
            print("error")
            # pyautogui.alert("ERROR")
            print(response.text)
            messages.info(request, 'ERROR')
            return HttpResponseRedirect('/share/'+id)
            # return Response({"error": "Request failed"}, status=response.status_code)
        
        
        

    return render(request,"QuestionElab/share.html", {
        "obj":obj,
        "resultmarkdown": valuemarkdown,
        "resultmarkdownbetween": valuemarkdownbetween,
        "resultmarkdownlast" : valuemarkdownlast,
        "resultoutput": valueoutput,
        "resultinput": valueinput,
        
    })
    
def editquestion(request , id):
    obj = Question.objects.get(question_token = id)
    
    if 'send' in request.POST:
        Qname = request.POST['Qname']
        Qlanguage = request.POST['Qlanguage']
        Qcondition = request.POST.getlist('Qcondition')
        Qelement = request.POST['Qelement']
        exactmacth = False
        ignorespace = False
        sensitive = False
        insensitive = False
        for x in range(len(Qcondition)):
            if Qcondition[x] == "exactmacth":
                exactmacth = True
            elif Qcondition[x] == "ignorespace":
                ignorespace = True
            elif Qcondition[x] == "sensitive":
                sensitive = True
            elif Qcondition[x] == "insensitive":
                insensitive = True
        source = request.POST['source']
        
        valuemarkdown = mdprocessmarkdown(source)
        valuemarkdownbetween = mdprocessmarkdownbetween(source)
        valuemarkdownlast = mdprocessmarkdownlast(source)
        valueoutput = mdprocessoutput(source)
        valueinput = mdprocessinput(source)

        context = {
            "Qname": Qname,
            "Qlanguage" : Qlanguage,
            "Qcondition" : Qcondition,
            "Qelement" : Qelement,
            "exactmacth" : exactmacth,
            "ignorespace" : ignorespace,
            "sensitive" : sensitive,
            "insensitive" : insensitive,
            "source": source,
            "resultmarkdown": valuemarkdown,
            "resultmarkdownbetween": valuemarkdownbetween,
            "resultmarkdownlast" : valuemarkdownlast,
            "resultoutput": valueoutput,
            "resultinput": valueinput,
            
        }
        
        return render(request,"QuestionElab/index.html", context=context)
    
    
    elif 'save' in request.POST:
        result_str = obj.question_token
        # result_str = randStr(chars='abcdefghijklmnopqrstuvwxyz1234567890') 
        username = request.session['username']
        Qlanguage = request.POST['Qlanguage']
        Qname = request.POST['Qname']
        Qcondition = request.POST.getlist('Qcondition')
        source = request.POST['source']
        Qelement = request.POST['Qelement']
        # valueoutput = mdprocessoutput(source)
        # valueinput = mdprocessinput(source)
        obj.question_language = Qlanguage
        obj.question_name = Qname
        obj.question_username = username
        obj.question_source = source
        obj.question_condition = Qcondition
        obj.question_element = Qelement
        obj.save()
        
      
        return redirect('manage')
    else :
        obj = Question.objects.get(question_token = id)
        Qname = obj.question_name
        Qlanguage = obj.question_language
        Qcondition = obj.question_condition
        source = obj.question_source
        Qelement = obj.question_element
        exactmacth = False
        ignorespace = False
        sensitive = False
        insensitive = False
        for x in Qcondition.replace("'",'').replace("[",'').replace("]",'').replace(" ",'').split(','):

            if x == "exactmacth":
                exactmacth = True
            elif x == "ignorespace":
                ignorespace = True
            elif x == "sensitive":
                sensitive = True
            elif x == "insensitive":
                insensitive = True
            
        valuemarkdown = mdprocessmarkdown(source)
        valueoutput = mdprocessoutput(source)
        valueinput = mdprocessinput(source)

        context = {
            "Qname": Qname,
            "Qlanguage" : Qlanguage,
        
            "exactmacth" : exactmacth,
            "ignorespace" : ignorespace,
            "sensitive" : sensitive,
            "insensitive" : insensitive,
            "source": source,
            "Qelement": Qelement,
            "resultmarkdown": valuemarkdown,
            "resultoutput": valueoutput,
            "resultinput": valueinput,
                
            }
      
    return render(request,"QuestionElab/index.html", context=context)
    

    
def searcheachquestion(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method == "POST" :
        username = request.session['username']
        search = request.POST["searcheachquestion"]
        searchs = Question.objects.filter(question_username = username).filter(question_name__contains=search)
        
        return render(request, "QuestionElab/manage.html", {
            "tables" : searchs

        })
    else :
        return HttpResponseRedirect(reverse("manage"))


# def error_404_view(request, exception):
   
#     # we add the path to the the 404.html file
#     # here. The name of our HTML file is 404.html
#     return render(request, 'QuestionElab/notfound.html')