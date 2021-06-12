from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf.urls import url,include
from django.conf import settings

urlpatterns = [
    path('',views.index, name='index'),
    path('eval',views.evaluateCode, name='eval'),
    path("register", views.register_request, name="register"),
    path("evaluator", views.evaluator, name="evaluator"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("Addproject", views.createproject, name= "Addproject"),
    path("dash", views.dashboard, name= "dash"),
    path("Profile", views.Profile, name= "Profile"),
    path("colorchecker", views.ccc, name= "colorchecker"),
    path("evalFromFile", views.evalFromFile, name= "evalFromFile"),
    path("WCAGChecklist", views.wcagchecklist, name= "WCAGChecklist"),
    path("RECTests", views.RECTests, name= "RECTests"),
    path("WCAGMap", views.WCAGMap, name= "WCAGMap"),
    path("GitClone", views.gitclone, name= "GitClone"),
    path("ShowScrapper", views.ShowScrapper, name= "ShowScrapper"),
    path("ShowCSSParser", views.ShowCSSParser, name= "ShowCSSParser"),
    path("CSSParser", views.CSSParser, name= "CSSParser"),
    path("Scrapper", views.Scrapper, name= "Scrapper"),
    url(r'^file/', include('filemanager.urls', namespace='filemanager'),name="f"),


]

# whenever 'localhost:8000' will be called, function named 'index' will be called that is present in 'views.py' file
# This will happen for all other routes as well
