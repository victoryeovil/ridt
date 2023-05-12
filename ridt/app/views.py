from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment, User
from .forms import BlogForm, CommentForm, CustomUserCreationForm
from django.utils import timezone

# Create your views here.
def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('website:index')
            else:
                return render(request, 'app/login.html', {'error': 'Invalid login credentials'})
        else:
            return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('website:index')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/register.html', {'form': form})


@login_required
def dashboard(request):
    blogs = Blog.objects.filter(created_by=request.user)
    comments = Comment.objects.filter(created_by=request.user)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'app/dashboard.html', {'blogs': blogs, 'comments': comments, 'users': users})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.created_by = request.user
            blog.save()
            return redirect('dashboard')
    else:
        form = BlogForm()
    return render(request, 'app/create_blog.html', {'form': form})

@login_required
def read_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=blog)
    return render(request, 'app/read_blog.html', {'blog': blog, 'comments': comments})


@login_required
def view_blog(request, blog_id):
    # Retrieve the blog post
    blog = get_object_or_404(Blog, id=blog_id)

    # Retrieve comments related to the blog post
    comments = Comment.objects.filter(blog=blog)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')

        # Create a new comment associated with the blog post
        comment = Comment.objects.create(blog=blog, user=request.user, text=comment_text)

        # Redirect to the same blog post after submitting the comment
        return redirect('view_blog', blog_id=blog_id)

    return render(request, 'app/view_blog.html', {'blog': blog, 'comments': comments})

@login_required
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.update_timestamp = timezone.now()
            blog.save()
            return redirect('dashboard')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'app/update_blog.html', {'form': form})

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect('dashboard')

@login_required
def create_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.created_by = request.user
            comment.save()
            return redirect('read_blog', blog_id=blog.id)
    else:
        form = CommentForm()
    return render(request, 'app/create_comment.html', {'form': form, 'blog': blog})

@login_required
def admin(request):
    if not request.user.is_superuser:
        return redirect('view_all_blogs')
    else:
        blogs = Blog.objects.all()
        comments = Comment.objects.all()
        users = User.objects.all()
    return render(request, 'app/admin.html', {'blogs': blogs, 'comments': comments, 'users': users})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin')

@login_required
def view_all_blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'app/view_all_blogs.html', {'blogs': blogs})

@login_required
def comment_on_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('view_all_blogs')
    else:
        return redirect('view_all_blogs')

    return render(request, 'app/comment.html', {'blog': blog, 'form': form})