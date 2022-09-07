from .models import Post, SubPost, Comment, Star, Category
from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import SubPostModelForm, PostCommentForm, PostForm
from django.shortcuts import get_object_or_404
# from django.http import HttpResponseRedirect
from email.policy import HTTP
import http
from http.client import HTTPResponse
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from .models import Post, SubPost, Comment
from django.utils.http import urlencode
from user.models import Profile


def flowchart(request):
    subpost = SubPost.objects.all()
    context = {'subpost': subpost}
    return render(request, 'post/flow2.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'post/landing.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context

def following_posts(request):
    posts=Post.objects.all()
    categories_list = Category.objects.all()
    following_profiles=Profile.objects.get(user=request.user).following.all()
    '''
    following_posts=[]
    for post in posts:
        if post.author.profile in following_profiles:
            following_posts.add(post.id)
    print(following_posts)
    '''
    context = {
        'posts':posts,
        'following_profiles': following_profiles,
        'categories_list':categories_list
        }
    return render(request, 'post/home.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'image', 'content','category']
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'New Post Created! Enter details.')
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object()).order_by('-created')
        if Star.objects.filter(posts=self.get_object(),user=self.request.user).exists():
            starred=True
        else:
            starred=False
        context['starred']=starred
        return context


@login_required
def postUpdateView(request, pk):
    context = {}
    obj = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, f'Post Updated!')
        return redirect('post-detail', pk=pk)
    context["form"] = form
    return render(request, "post/post_update.html", context)


@login_required
def deletePost(request, pk):
    post = Post.objects.get(id=pk).delete()
    messages.success(request, f'Your Post information has been deleted')
    return redirect('user-home')


class SubPostCreateView(CreateView):
    model = SubPost
    form_class = SubPostModelForm
    template_name = 'post/subpost_form.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = "/post/{post_id}"


@login_required
def updateSubpost(request, pk, id):
    subpost = SubPost.objects.get(id=id)
    context = {}
    form = SubPostModelForm(request.POST or None, instance=subpost)
    if form.is_valid():
        form.save()
        messages.success(request, f'Subpost updated!')
        return redirect('post-detail', pk=pk)
    context["form"] = form
    return render(request, "post/subpost_update.html", context)

@login_required
def deleteSubpost(request, pk, id):
    subpost = SubPost.objects.get(id=id).delete()
    messages.success(request, f'Your subpost information has been deleted')
    return redirect('post-detail', pk=pk)


def search(request):
    query = request.GET['query']
    # allposts=Post.objects.all()
    allposts = Post.objects.filter(title__icontains=query)
    print(allposts)
    context = {'allpost': allposts}
    return render(request, 'post/search.html', context)
    # return HttpResponse('This is search')


def postComment(request, pk):
    if request.method == "POST":
        body = request.POST.get('body')
        if body == "":
            messages.success(request, "Comment cannot be empty!")
            # return HttpResponseRedirect(reverse('post-details-comment') + '#' + urlencode({'next': comments}))
            return redirect('post-detail-comment', pk=pk)
        else:
            user = request.user
            postSno = request.POST.get('postSno')
            post = Post.objects.get(pk=pk)
            comment = Comment(body=body, user=user, post=post)
            comment.save()
            messages.success(request, "Comment posted successfully!")
        return redirect('post-detail', pk=pk)


# def get_redirect_url(*args, **kwargs):
#     hash_part = "add_data_Modal"  # the data you want to add to the hash part
#     return reverse("createpost") + "#{0}".format(hash_part)

@login_required
def star(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    current_stars = post.stars_count
    s, created = Star.objects.get_or_create(user=user)
    if s.posts.filter(id=pk).exists():
        s.posts.remove(post)
        current_stars = current_stars-1
        messages.success(request, f'Post removed from Starred Posts List!')
    else:
        s.posts.add(post)
        current_stars = current_stars+1
        messages.success(request, f'Post added to Starred Posts List!')
    post.stars_count = current_stars
    post.save()
    return redirect('post-detail', pk=pk)


@login_required
def starlist(request):
    star_list = Star.objects.get(user=request.user)
    return render(request, "post/stars.html", {'star_list': star_list})


def categoryList(request, slug):
    category = Category.objects.get(slug=slug)
    category_posts = Post.objects.filter(category=category)
    return render(request, "post/categories.html", {'category_posts': category_posts})

'''
def landing(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'post/landing.html', context)
'''

def explore(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'post/explore.html',context)