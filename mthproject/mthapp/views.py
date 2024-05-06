from django.contrib import auth, messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from .forms import ProfileForm,PForm
# from requests import post

from . models import Post,Profile,Comment,NewManager
from . forms import Postform
from .forms import *


def navbar_with_dropdown(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})

# Create your views here.
def home(request):
    posts = Post.objects.all()
    member=User.objects.all()
    return render(request,"index.html",{'posts':posts,'member':member})

def index(request):
    user_object = User.objects.get(username=request.user.username)
    categories = Category.objects.all()  # Retrieve all categories
    posts_by_category = {}  # Dictionary to store posts for each category
    for category in categories:
        posts_by_category[category] = Post.objects.filter(category=category)
    # user_profile = Profile.objects.get(user=user_object)

    # post= get_object_or_404(Post,id=id)
    # post_id=Post.id

    # if post.fav.filter(id=request.user.id).exists():
    #     is_fav=True
    posts = Post.objects.all()
    allmovies=[]
    categories=Post.objects.values('category')
    # cats = {item['categories'] for item in catmovies}
    # for cat in cats:
    #     movie=Post.objects.filter(categories=cat)
    #     allmovies.append(movie)
    # return render(request,'index.html',{'posts':posts})

    return render(request,'index.html',{'posts_by_category':posts_by_category})
def add_post(request):
    if request.method == 'POST':
        form = PForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Create an instance of the post model but don't save it to the database yet
            post.author = request.user  # Set the author field to the currently logged-in user
            post.save()
            # form.save()
            return redirect('mthapp:index')  # Assuming you have a URL named 'post_list' for listing posts
    else:
        form = PForm()
    return render(request, 'add_post_dummy.html', {'form': form})

# def post_list(request):
#     user_object = User.objects.get(username=request.user.username)
#     posts = Post.objects.all()
#     return render(request,'index.html',{'posts':posts})



# def upload(request):
#     if request.method == 'POST':
#         author = User.objects.get(username=request.user.username)
#         moviename = request.POST.get('moviename')
#         descriptions = request.POST['descriptions']
#         categories = request.POST['categories']
#         actors_name = request.POST['actors_name']
#         youtube_link = request.POST['youtube_link']
#         images = request.FILES.get('post_images')
#         rdate = request.POST['rdate']
#
#         new_post = Post.objects.create(author=author,moviename=moviename, descriptions=descriptions, categories=categories,
#                                        actors_name=actors_name, youtube_link=youtube_link, images=images, rdate=rdate)
#         new_post.save()
#         return redirect('mthapp:index')
#
#     return render(request,'addmovie.html')

def detail(request,movieid):
    com=Comment.objects.all()
    movie=Post.objects.get(id=movieid)
    # profile=Profile.objects.get(user=request.user)
    comments=Comment.objects.filter(post=movie).order_by('-id')
    comment_form = Commentformm()

    if request.method=='POST':
        comment_form=Commentformm(request.POST or None)
        if comment_form.is_valid():
            content=request.POST.get('content')
            comment=Comment.objects.create(post=movie,author=request.user,content=content)
            comment.save()
            # return HttpResponseRedirect(movie.get_absolute_url())
        else:
            comment_form=Commentformm()
    return render(request,"detail.html",{'movie':movie,'comments':comments,'comment_form':comment_form,'com':com})

@login_required
def favourites(request,id):
            post = get_object_or_404(Post, id=id)
            if post.favourites.filter(id=request.user.id).exists():
                post.favourites.remove(request.user)
            else:
                post.favourites.add(request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required()
def favourite_list(request):
    new=Post.newmanager.filter(favourites=request.user)
    return render(request,'favourites.html',{'new':new})



def update(request,id):
    movie=Post.objects.get(id=id)
    form= Postform(request.POST or None, request.FILES,instance=movie)
    if form.is_valid():
        form.save()
        return redirect('mthapp:index')
    return render(request,'edit.html',{'form':form,'movie':movie})

def delete(request, id):
    if request.method=='POST':
        movie=Post.objects.get(id=id)
        movie.delete()
        return redirect('mthapp:index')
    return render(request,'delete.html')
def deletecomment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    movieid = comment.post.id
    return redirect('mthapp:detail',movieid=movieid)

    # if request.method=='POST':
    #     comment=Comment.objects.get(id=id)
    #     comment.delete()
    #     movieid = comment.post.id
    #     return redirect('mthapp:detail',movieid=movieid)
    # return render(request,'delete.html')
@login_required
def profile_page(request):
    user_posts = Post.objects.filter(author=request.user)
    user_profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') is not None:
            image = request.FILES['image']
        else:
            image=user_profile.profile_picture
        location = request.POST.get('location','')

        user_profile.profile_picture = image
        user_profile.location = location

        user_profile.save()
    return render(request, 'profile_page.html', {'user_posts': user_posts,'user_profile':user_profile})

@login_required(login_url='login')
def settings(request):
    # user_profile = Profile.objects.get(user=request.user)
    user_profile= get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        # if request.FILES.get('image') == None:
        #     image = user_profile.profile_picture
        #     location = request.POST['location']
        #
        #     user_profile.profile_picture = image
        #     user_profile.location = location
        #     user_profile.save()
        if request.FILES.get('image') is not None:
            image = request.FILES['image']
        else:
            image=user_profile.profile_picture
        location = request.POST.get('location','')

        user_profile.profile_picture = image
        user_profile.location = location
        user_profile.save()

        return redirect('mthapp:settings')
    return render(request, 'settings.html', {'user_profile': user_profile})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('mthapp:index')
        else:
            messages.info(request, "Invalid Credentials.")
            return redirect('/')
    else:
        return render(request, "login.html")
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        last_name = request.POST['last_name']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if password == c_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username exists.")
                return redirect('mthapp:signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email exists.")
                return redirect('mthapp:signup')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                # return redirect('profapp:profile')
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('mthapp:login')
        else:
            messages.info(request, "Both passwords not matching")
            return redirect('mthapp:signup')


    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('mthapp:login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mthapp:settings')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def change_username(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mthapp:settings')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'change_username.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return redirect('mthapp:settings')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})