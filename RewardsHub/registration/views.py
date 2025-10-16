from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpRequest

# Create your views here.
def sign_in(req: HttpRequest):
    if req.method == "POST":
        # TODO Create user and log them in
        print(req.POST)
        user = User.objects.create_user(
            username=req.POST.get("email"),
            password=req.POST.get("password"),
            email=req.POST.get("email"),
            first_name=req.POST.get("first_name"),
            last_name=req.POST.get("last_name"),
        )
        login(req, user)
        # TODO: Redirect to home page
    else: 
        # TODO: Redirect to sign in page
        pass

def sign_up(req: HttpRequest):
    if req.method == "POST":
        # TODO Sign a user in
        user = authenticate(req, username=req.POST.get("email"), password=req.POST.get("password"))
        if user is not None:
            login(req, user)
            return redirect("/")
        # TODO: Redirect to Expo 
    else:
        # TODO: Redirect to Expo Sign in Page
        pass