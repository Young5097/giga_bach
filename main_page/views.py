from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FindUsernameForm, SignUpForm, UserProfileForm, User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from board_page.models import Post as BoardPagePost


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
            # 회원가입 성공 후 자동으로 로그인
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})


# 아이디 찾기 뷰
def find_username_view(request):
    username = None

    if request.method == "POST":
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            email = form.cleaned_data["email"]

            # 아이디를 first_name과 email로 찾기
            username = (
                User.objects.filter(first_name=first_name, email=email)
                .values_list("username", flat=True)
                .first()
            )

    else:
        form = FindUsernameForm()

    return render(
        request, "users/find_username.html", {"form": form, "username": username}
    )


# 마이페이지 뷰 (로그인 필수)
def mypage_view(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, "users/mypage.html", {"form": form})


def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("mypage")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # 회원 삭제
        logout(request)  # 로그아웃
        return redirect("main")  # 사용자를 홈 페이지로 리다이렉트

    return render(request, "users/delete_account.html")
