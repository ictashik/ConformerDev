import os
import datetime
from bs4 import BeautifulSoup
from collections import Counter
from collections import OrderedDict
import urllib.request
import re
from django.conf import settings
from pathlib import Path
from git.repo.base import Repo
from django.shortcuts import render
from calculator.models import Project,Error,Test
from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
import automated_accessibility_testing
from wcag_zoo.validators.anteater import Anteater
from wcag_zoo.validators.ayeaye import Ayeaye
from wcag_zoo.validators.glowworm import Glowworm
from wcag_zoo.validators.molerat import Molerat
from wcag_zoo.validators.anteater import Anteater
from filemanager import settings as FMS

#Functions

def countfiles(extension):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    PARENT_MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
    MEDIA_ROOT = os.path.join(PARENT_MEDIA_ROOT, 'media')
    count=0
    for root, dirs, files in os.walk(MEDIA_ROOT):
	       for file in files:
		             if(file.endswith(extension)):
			                      count+=1
    return count





#View Files
def index(request):
    objs=Project.objects.all()
    projectsCount = Project.objects.count()
    testCount = Test.objects.count()
    errorCount = Error.objects.count()
    aeCount = Error.objects.filter(errorType__contains='AcessibilityException').count()
    svCount = Error.objects.filter(errorType__contains='StaticHTMLValidation').count()
    errs=Error.objects.all()
    MAT= Error.objects.filter(errorText__contains='Missing alt atribute on tag').count()
    MHT= 0
    HER= Error.objects.filter(errorText__contains='Suspected hierarchical order').count()
    COL= 0
    OBS= Error.objects.filter(errorText__contains='obsolete').count()
    TIT= Error.objects.filter(errorText__contains='Missing header tag').count() + Error.objects.filter(errorText__contains='element has no cells beginning on it').count()+Error.objects.filter(errorText__contains='unclosed').count()
    return render(request,'dash.html',{'objs':objs,'projectsCount':projectsCount,'testCount':testCount,'errorCount':errorCount,'aeCount':aeCount,'svCount':svCount,"MAT":MAT,"MHT":MHT,"HER":HER,"COL":COL,"OBS":OBS,"TIT":TIT})

def ccc(request):
    return render(request,'colorchecker.html')


def evalFromFile(request):
    path = request.POST['path']

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    PARENT_MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
    REAL_MEDIA_PATH = PARENT_MEDIA_ROOT + path

    with open(REAL_MEDIA_PATH, "r", encoding='utf-8') as f:
        code= f.read()
    res = automated_accessibility_testing.check_accessibility(code)

    soup = BeautifulSoup(code)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    length = len(code.split('\n'))
    AccessibilityExceptionCount=0
    StaticHTMLValidationCount=0
    MAT =0
    MHT=0
    HER =0
    COL=0
    OBS=0
    TIT=0
    username = None
    username = request.user.username
    t = Test()
    newTestID =  Test.objects.count() +1


    for item in res:
        newlist = str(item).split(":")
        error=Error()
        error.testID=newTestID
        error.errorType = newlist[0]
        if( 'AcessibilityException' in error.errorType): AccessibilityExceptionCount+=1
        if('StaticHTMLValidation' in error.errorType): StaticHTMLValidationCount+=1
        error.TestID=int(newTestID)
        error.errorText = newlist[2:]
        error.errorLocation = newlist[1]
        error.testDateTime = datetime.datetime.now().time()
        if('alt' in str(error.errorText)): MAT+=1
        if('Element “title” must not be empty' in str(error.errorText)): TIT+=1
        if('obsolete' in str(error.errorText)): OBS+=1
        if('Suspected hierarchical order' in str(error.errorText)): HER+=1
        if('Missing header tag H1' in str(error.errorText)): HER+=1
        if('unclosed' in str(error.errorText)): TIT+=1
        if('element has no cells beginning on it' in str(error.errorText)): TIT+=1


        error.save()


    test=Test()
    test.testID = int(newTestID)
    test.userName = username
    test.testFileURL =  REAL_MEDIA_PATH
    test.totalLines = length
    test.AccessibilityExceptionCount = AccessibilityExceptionCount
    test.StaticHTMLValidationCount = StaticHTMLValidationCount
    test.save()





    history = Test.objects.filter(testFileURL=REAL_MEDIA_PATH).order_by('-testDateTime')


    return render(request, "result.html", {"result": res,"code":code,"length":length,"AccessibilityExceptionCount":AccessibilityExceptionCount,"StaticHTMLValidationCount":StaticHTMLValidationCount,"history":history,"MAT":MAT,"MHT":MHT,"HER":HER,"COL":COL,"OBS":OBS,"TIT":TIT,"links":links})


def evaluateCode(request):
    code = request.POST['code']
    res = automated_accessibility_testing.check_accessibility(code)
    return render(request, "result.html", {"result": res,"code":code})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="register.html", context={"register_form":form})

def ShowScrapper(request):
    return render(request,"Webscrapper.html")

def ShowCSSParser(request):
    return render(request,"CSSParser.html")

def CSSParser(request):
    if request.method == "POST":
        if request.POST.get('csscode'):
            text= request.POST.get('csscode')
            r = re.compile(r'#[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}')
            a = r.findall(text)
            my_dict = dict( [ (i, a.count(i)) for i in set(a) ] )
            colors = dict(sorted(my_dict.items(),  key = lambda kv: kv[1], reverse = True))
            topten = dict(sorted(my_dict.items(),  key = lambda kv: kv[1], reverse = True)[:10])
            return render(request,"CSSParser.html",{"colors":colors,"TT":topten})

def Scrapper(request):
    if request.method == "POST":
        if request.POST.get('url'):
            try:
                url = request.POST.get('url')
                html_page = urllib.request.urlopen(url)
                soup = BeautifulSoup(html_page)
                links = []

                for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                    links.append(link.get('href'))

                return render(request,"Webscrapper.html",{"links":links})
            except:
                messages.error(request, "Unsuccessful registration. Invalid information.")
                return render(request,"Webscrapper.html",{"links":'Error: Link Cant be Scrapped'})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("login")

def createproject(request):
        if request.method == 'POST':
            if request.POST.get('protitle') and request.POST.get('prodesc') and request.POST.get('progit'):
                project=Project()
                project.title= request.POST.get('protitle')
                project.description= request.POST.get('prodesc')
                project.git_url = request.POST.get('progit')
                project.save()

                BASE_DIR = os.path.dirname(os.path.realpath(__file__))
                MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
                PARENT_MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
                REAL_MEDIA_PATH = os.path.join(PARENT_MEDIA_ROOT, 'media//uploads//')
                try:
                    os.mkdir(os.path.join(REAL_MEDIA_PATH, project.title))
                except:
                    messages.info(request, "Error Creating Folder")



                messages.info(request, "Added Project Directory")
                objs=Project.objects.all()
                projectsCount = Project.objects.count()
                testCount = Test.objects.count()
                errorCount = Error.objects.count()
                aeCount = Error.objects.filter(errorType__contains='AcessibilityException').count()
                svCount = Error.objects.filter(errorType__contains='StaticHTMLValidation').count()
                return render(request,'dash.html',{'objs':objs,'projectsCount':projectsCount,'testCount':testCount,'errorCount':errorCount,'aeCount':aeCount,'svCount':svCount})
        else:
                return render(request,'Addproject.html')
                messages.info(request, "Error Adding Project")

def RECTests(request):
    username = request.user.username
    tst = Test.objects.filter(userName=username).order_by('-testDateTime')
    return render(request, 'RECTests.html',{'tst':tst})


def dashboard(request):
    objs=Project.objects.all()
    projectsCount = Project.objects.count()
    testCount = Test.objects.count()
    errorCount = Error.objects.count()
    aeCount = Error.objects.filter(errorType__contains='AcessibilityException').count()
    svCount = Error.objects.filter(errorType__contains='StaticHTMLValidation').count()
    errs=Error.objects.all()
    MAT= Error.objects.filter(errorText__contains='alt').count()
    MHT= 0
    HER= Error.objects.filter(errorText__contains='Suspected hierarchical order').count()
    COL= 0
    OBS= Error.objects.filter(errorText__contains='obsolete').count()
    TIT= Error.objects.filter(errorText__contains='Missing header tag').count() + Error.objects.filter(errorText__contains='element has no cells beginning on it').count()+Error.objects.filter(errorText__contains='unclosed').count()
    return render(request,'dash.html',{'objs':objs,'projectsCount':projectsCount,'testCount':testCount,'errorCount':errorCount,'aeCount':aeCount,'svCount':svCount,"FCHTML":countfiles('.html'),"FCCSS":countfiles('.css'),"FCJS":countfiles('.js'),"FCPNG":countfiles('.png'),"FCJPG":countfiles('.jpg'),"FCTTF":countfiles('.ttf'),"MAT":MAT,"MHT":MHT,"HER":HER,"COL":COL,"OBS":OBS,"TIT":TIT})

def evaluator(request):
    return render(request,'input.html')

def WCAGMap(request):
    return render(request,'WCAGMap.html')

def wcagchecklist(request):
    return render(request,'WCAGChecklist.html')

def Profile(request):
    username = None
    return render(request,'profile.html',{"username":username})

def gitclone(request):
    if request.method == 'POST':
        if request.POST.get('HFIDtitle') and request.POST.get('HFIDgit'):
            vtitle = request.POST.get('HFIDtitle')
            vgit =  request.POST.get('HFIDgit')
            BASE_DIR = os.path.dirname(os.path.realpath(__file__))
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
            PARENT_MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
            REAL_MEDIA_PATH = os.path.join(PARENT_MEDIA_ROOT, 'media//uploads//')
            prdir = os.path.join(REAL_MEDIA_PATH, vtitle)
            try:
                Repo.clone_from(vgit, prdir)
            except:
                messages.info(request, "Error")

            return render(request,'cloneSuccess.html',{"title":vtitle})
    else:
        objs=Project.objects.all()
        projectsCount = Project.objects.count()
        testCount = Test.objects.count()
        errorCount = Error.objects.count()
        aeCount = Error.objects.filter(errorType__contains='AcessibilityException').count()
        svCount = Error.objects.filter(errorType__contains='StaticHTMLValidation').count()
        messages.info(request, "Error Cloning!!")
        return render(request,'dash.html',{'objs':objs,'projectsCount':projectsCount,'testCount':testCount,'errorCount':errorCount,'aeCount':aeCount,'svCount':svCount})
