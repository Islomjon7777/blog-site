from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm, CommentForm
from .models import *

# Create your views here.
# HOME VIEW
@login_required(login_url="login/")
def HomeView(request):
    post_yaxshi = PostlarModel.objects.filter(turi="yaxshi")
    post_yaxshi_count = PostlarModel.objects.filter(turi="yaxshi").count()
    post_yomon = PostlarModel.objects.filter(turi="yomon")
    post_yomon_count = PostlarModel.objects.filter(turi="yomon").count()

    ctx = {
        'yaxshi': post_yaxshi,
        'yaxshi_count': post_yaxshi_count,
        'yomon': post_yomon,
        'yomon_count': post_yomon_count,
    }

    return render(request, 'home.html', ctx)




# LOGIN UCHUN VIEW
def LoginView(request):
    if request.POST:
        userName = request.POST['username']
        userPassword = request.POST['password']
        user = authenticate(request, username=userName, password=userPassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Akkaunt muvofaqiyatli kirdingiz.")
            return redirect('/')
        else:
            messages.success(request, "Login yoki parol xato.")
            return redirect('login')
    else:
        return render(request, 'login.html')



# LOGOUT UCHUN VIEW
def LogoutView(request):
    logout(request)
    return render(request, 'home.html')


# REGISTRATSIYA UCHUN VIEW
def RegisterView(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akkaunt muvoffaqiyatli ro'yxatdan o'tdi.")
            return redirect('login')
        else:
            messages.error(request, "Hamma joyni to'ldiring.")
            return redirect('register')
        
    else:
        form = RegisterForm()
    
    ctx = {
        "forms": form
    }

    return render(request, 'register.html', ctx)


@login_required(login_url='/login')
def ProfileView(request, pk):
    userEdit = Profile.objects.get(user_id=pk)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=userEdit)
        if form.is_valid():
            form.save()
            messages.success(request, "Account muvoffaqiyatli yangilandi!")
            return redirect('profile', pk=userEdit.user_id)
        else:
            messages.error(request, "Hamma joyni to'ldiring!")
            return redirect('profile', pk=userEdit.user_id)
        
    form = ProfileForm(instance=userEdit)

    ctx = {
        "forms": form
    }

    return render(request, 'profile.html', ctx)






# comment
@login_required(login_url='/login')
def CommentView(request,pk):
    post_s = PostlarModel.objects.get(id=pk)
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=True)
            data.post = PostlarModel.objects.get(id=pk)
            data.profile = Profile.objects.get(id=request.user.id)
            data.save()
            return redirect('comment', pk)
        else:
            return redirect('comment', pk)
    
    comment_id = CommentModel.objects.filter(post_id=pk)
    comment_id_count = CommentModel.objects.filter(post_id=pk).count()
    form = CommentForm()
    
    ctx = {
        'forms': form,
        'posts': post_s,
        'comment_id': comment_id,
        'comment_count': comment_id_count,
    }

    return render(request,'comment.html',ctx)



@login_required(login_url='/login')
def EditCommentsView(request, pk):
    editcomment = CommentModel.objects.get(id=pk)
    if request.POST:
        form = CommentForm(request.POST, instance=editcomment)
        if form.is_valid():
            form.save()
            messages.success(request, "comment muvoffaqiyatli yangilandi!")
            return redirect('comment', request.user.id)
        else:
            messages.success(request, "comment muvoffaqiyatli yangilandi!")
            return redirect('EditComments', pk=editcomment.id)
        
    form = CommentForm(instance=editcomment)

    ctx = {
        'forms': form,
        'pk': pk
    }
    return render(request, 'edit_comment.html', ctx)