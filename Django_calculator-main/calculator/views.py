from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this

from wcag_zoo.validators.anteater import Anteater
from wcag_zoo.validators.ayeaye import Ayeaye
from wcag_zoo.validators.glowworm import Glowworm
from wcag_zoo.validators.molerat import Molerat
from wcag_zoo.validators.anteater import Anteater

# Create your views here.

def index(request):
    return render(request, "input.html")


def addition(request):

    code = request.POST['code']

    a = Anteater()
    b = Ayeaye()
    c = Glowworm()
    d = Molerat()
    my_html = b'code'
    ra = a.validate_document(my_html)
    rb = b.validate_document(my_html)
    rc = c.validate_document(my_html)
    rd = d.validate_document(my_html)

    res = dict(list(ra.items()) + list(rb.items()))
    return render(request, "result.html", {"result": res})

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
