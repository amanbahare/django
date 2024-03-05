from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import PostForm
from .models import Post, CustomUser
from django.utils import timezone


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form, 'post': post})
    else:
        return redirect('post_list')

def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('post_list')

        myuser = CustomUser.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        # messages.success(request, "Signup successful! Please login.")
        return redirect('login')  # Redirect to your login page URL
    else:
        return render(request, 'blog/signup.html')  # Render your signup form template

def handleLogin(request):
    if request.method == "POST":
        username = request.POST['loginusername']
        password = request.POST['loginpass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('post_list')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')  # Redirect to your login page URL
    else:
        return render(request, 'blog/login.html')  # Render your login form template

def handleLogout(request):
    logout(request)
    return redirect('post_list')

@login_required
def profile(request):
    user = request.user
    return render(request, 'blog/profile.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if new_password:
            user.set_password(new_password)
        user.save()

        return redirect('post_list')

    return render(request, 'blog/profile.html')




# from django.shortcuts import render ,get_object_or_404
# from django.shortcuts import redirect
# from .models import Post
# from django.utils import timezone
# from .forms import PostForm
# from django.utils.text import Truncator
# from .models import CustomUser
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseNotFound,HttpResponseRedirect
# from django.urls import reverse_lazy, reverse


# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})

# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# from django.contrib.auth.decorators import login_required

# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # Check if the current user is the author of the post
#     if request.user == post.author:
#         if request.method == "POST":
#             form = PostForm(request.POST, instance=post)
#             if form.is_valid():
#                 post = form.save(commit=False)
#                 post.author = request.user
#                 post.published_date = timezone.now()
#                 post.save()
#                 return redirect('post_detail', pk=post.pk)
#         else:
#             form = PostForm(instance=post)
#         return render(request, 'blog/post_edit.html', {'form': form, 'post': post})
#     else:
#         # If the current user is not the author, redirect them homepage
#         return redirect('post_list') 


# def handleSignUp(request):
#     if request.method=="POST":
#         # Get the post parameters
#         username=request.POST['username']
#         email=request.POST['email']
#         fname=request.POST['fname']
#         lname=request.POST['lname']
#         pass1=request.POST['pass1']
#         pass2=request.POST['pass2']


#         if (pass1!= pass2):
#              messages.error(request, "Passwords do not match")
#              return redirect('post_list')
        
#         # Create the user
#         myuser = CustomUser.objects.create_user(username, email, pass1)
#         myuser.first_name= fname
#         myuser.last_name= lname
#         myuser.save()
#         messages.success(request, " now click on login")
#         return redirect('post_list')

#     else:
#         return HttpResponseNotFound('<h1>Page not found</h1>')


# def handleLogin(request):
#     if request.method == "POST":
#         username = request.POST['loginusername']
#         password = request.POST['loginpass']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login successful!")

#             return redirect('post_list')
#         else:
#             messages.error(request, "Invalid credentials. Please try again.")
#             return redirect('post_list')

# def handleLogout(request):
#     logout(request)
#     # Redirect to the homepage or any other desired page after logout
#     return redirect('post_list')


# @login_required
# def profile(request):
#     user = request.user
#     return render(request, 'blog/profile.html', {'user': user})

# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         user = request.user
#         # Retrieve form data from POST request
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         new_password = request.POST.get('password')

#         # Update user's profile
#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         if new_password:
#             user.set_password(new_password)
#         user.save()

#         # Redirect to the profile page
#         return redirect(reverse('post_list'))

#     # Render the profile edit form for GET requests
#     return render(request, 'blog/profile.html')