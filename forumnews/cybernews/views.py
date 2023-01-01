from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comment, upVote
from django.contrib.auth.models import User
from django.template import loader
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404


def home_view(request):
    template = loader.get_template('forumnews/home.html')
    post_list = Post.objects.all().order_by('-post_date')
    context = {'post_list' : post_list}
    return HttpResponse(template.render(context, request))



@login_required
def delete_comment_view(request, commentid):

    comment = get_object_or_404(Comment, pk=commentid)
    comment_post = comment.comment_post
    comment_user = comment.comment_author
    post = get_object_or_404(Post, pk=comment_post.id)
    if request.user.is_authenticated and request.user == comment_user:
        comment.delete()
        return HttpResponseRedirect(reverse('post', args=[post.id]))

    template = loader.get_template('forumnews/unauth.html')
    return HttpResponse(template.render({}, request), status=401)   

@login_required
def update_comment_view(request, commentid):
    comment = get_object_or_404(Comment, pk=commentid)
    comment_user = comment.comment_author

    form = CommentForm(request.POST or None, instance=comment)
    if request.user.is_authenticated and request.user == comment_user:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('comment', args=[commentid]))
    else:
        template = loader.get_template('forumnews/unauth.html')
        return HttpResponse(template.render({}, request), status=401)
    
    template = loader.get_template('forumnews/update_comment.html')
    return HttpResponse(template.render({'form' : form}, request))

@login_required
def delete_post_view(request, postid):
    post = get_object_or_404(Post, pk=postid)
    post_user = post.post_author
    if request.user.is_authenticated and request.user == post_user:
        post.delete()
        return HttpResponseRedirect(reverse('home'))

    template = loader.get_template('forumnews/unauth.html')
    return HttpResponse(template.render({}, request), status=401)  

@login_required
def update_post_view(request, postid):
    post = get_object_or_404(Post, pk=postid)
    post_user = post.post_author
    form = PostForm(request.POST or None, instance=post)
    if request.user.is_authenticated and request.user == post_user:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post', args=[postid]))
    else:
        template = loader.get_template('forumnews/unauth.html')
        return HttpResponse(template.render({}, request), status=401)
    
    template = loader.get_template('forumnews/update_post.html')
    return HttpResponse(template.render({'form' : form}, request))



def post_view(request, postid):
    post = get_object_or_404(Post, pk=postid)
    comments = Comment.objects.filter(comment_post_id=postid)

    comment_count = comments.count()
    template = loader.get_template('forumnews/post_view.html')

    context = {
        'post' : post,
        'comments' : comments,
        'comment_count': comment_count
    }

    if request.method == 'POST':
        # Check if user is authenticated before parsing and saving form
        # if not redirect using reverse_lazy to the login page
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                current_comment = form.save(commit=False)
                current_comment.comment_author = request.user
                current_comment.comment_post = post
                current_comment.save()
                return HttpResponseRedirect(reverse('post', args=[postid]))
        else:
            return HttpResponseRedirect(reverse_lazy("login"))

    
    return HttpResponse(template.render(context, request))


@login_required
def add_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            current_post = form.save(commit=False)
            current_post.post_author = request.user
            current_post.save()
            redirect_link = reverse('post', args=[current_post.pk])
            return HttpResponseRedirect(redirect_link)
    else:
        form = PostForm()
    return render(request, 'forumnews/forms/add_post.html', {'form' : form})


def profile_view(request, username=''):
    usernameinfo = request.user
    if username:
        usernameinfo = User.objects.get(username=username)

    template = loader.get_template('forumnews/user_page.html')
    comments = Comment.objects.filter(comment_author=usernameinfo).count()
    posts = Post.objects.filter(post_author=usernameinfo).count()
    context = {'usernameinfo' : usernameinfo, 'comments' : comments, 'posts' : posts}

    return HttpResponse(template.render(context, request))


@login_required
def display_comment(request, id):
    template = loader.get_template("forumnews/display_comment.html")
    comment = Comment.objects.filter(id=id)[0]
    post = Post.objects.filter(id=comment.comment_post_id)[0]
    context = {'comment' : comment}

    if request.method == 'POST':
        # Check if user is authenticated before parsing and saving form
        # if not redirect using reverse_lazy to the login page
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                current_comment = form.save(commit=False)
                current_comment.comment_author = request.user
                current_comment.comment_post = post
                current_comment.parent_id = id
                current_comment.save()
                return HttpResponseRedirect(reverse('post', args=[post.id]))
        else:
            return HttpResponseRedirect(reverse_lazy("login"))
    return HttpResponse(template.render(context, request))


@login_required
def upvote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    upvote = upVote.objects.filter(upvote_user=user, upvote_post=post).first()
    if upvote:
        print("ALREADY upvoted")
        post.post_points -= 1
        post.save()
        upvote.delete()
        return HttpResponseRedirect(reverse('post', args=[post_id]))
    else:
        print("upvote!!!")
        new_upvote = upVote(upvote_user=user, upvote_post=post)
        post.post_points += 1
        post.save()
        new_upvote.save()
        return HttpResponseRedirect(reverse('post', args=[post_id]))


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
