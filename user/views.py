from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from post.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from post.models import Post
from .models import Profile
from django.http import HttpResponseRedirect

def login_home(request):
    post = Post.objects.all()
    context={'posts':post}
    return render(request, 'user/home.html',context)

def login_about(request):
    return render(request, 'user/about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

def login_about(request):
    return render(request, 'user/about.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user/profile.html', context)

@login_required
def userInfo(request,pk):
    user=Post.objects.get(id=pk).author
    profile=Profile.objects.get(user=user)
    posts=Post.objects.filter(author=user)
    context={
        'user':user,
        'profile':profile,
        'posts':posts
        }
    return render(request,'user/user_info.html',context)

@login_required
def follow(request,id):
    author =Profile.objects.get(id=id)
    currentUser = Profile.objects.get(user=request.user)
    followers = author.followers.all()
    if author != currentUser:
        if currentUser in followers:
            author.followers.remove(currentUser.id)
            messages.success(request, f'You unfollowed a user!')
        else:
            author.followers.add(currentUser.id)
            messages.success(request, f'You followed a user!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))