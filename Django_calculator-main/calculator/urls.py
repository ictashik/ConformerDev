from django.urls import path

from . import views     # it means - 'from all import views'

urlpatterns = [
    path('',views.index, name='index'),
    path('add',views.addition, name='add'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),

]

# whenever 'localhost:8000' will be called, function named 'index' will be called that is present in 'views.py' file
# This will happen for all other routes as well
