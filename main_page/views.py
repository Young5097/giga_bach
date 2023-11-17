from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import SignUpForm, FindUsernameForm
from django.contrib.auth.models import User


# Create your views here.
def main(request):
    return render(request, "main/main.html")


# 로그인 뷰
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "로그인 성공!")
            return redirect("/")  # 로그인 후 리다이렉트할 페이지
        else:
            messages.error(request, "로그인 실패. 아이디 또는 비밀번호를 확인하세요.")

    return render(request, "users/login.html")


# 회원가입 뷰
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")  # 회원가입 후 리다이렉트할 페이지
    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})


# 아이디 찾기
def find_username_view(request):
    if request.method == "POST":
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name", "")
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(name=name, email=email)
                return HttpResponse(f"찾은 사용자 이름: {user.username}")
            except User.DoesNotExist:
                return HttpResponse("해당하는 사용자를 찾을 수 없습니다.")

    return render(request, "users/find_username.html", {"form": form})
