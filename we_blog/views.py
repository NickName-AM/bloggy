from django.shortcuts import redirect, render
from we_blog.models import OurBlog, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random

# Create your views here.

# Home page
def we_blog(request):
    our_blogs = OurBlog.objects.all()
    if request.method == 'GET':
        # Try to choose 10 random blogs
        try:
            b_logs = random.sample(list(our_blogs), 10)
        # There might not even be 10 blogs. So, send as much blog you have (i.e less than 10)
        except Exception:
            b_logs = our_blogs

        # Choose ONE comment from every blog (Only ONE)
        return render(request, 'general/home.html', {'blogs': b_logs})

@login_required
def comment(request, b_id):
    uza = User.objects.get(id=request.user.id)
    b_log = OurBlog.objects.get(id=b_id)
    if request.method == 'GET':
        return redirect('home')
    elif request.method == 'POST':
        cmt = request.POST['cmt']
        Comment.objects.create(comment_content=cmt, writer=uza, blog=b_log)
        messages.success(request, 'Comment was added.')
        return redirect('show_blog',b_id=b_id)

@login_required    
def comment_delete(request, c_id):
    try:
        cmt = Comment.objects.get(id=c_id)
        if request.user.id == cmt.writer.id:
            cmt.delete()
            messages.success(request, 'Comment deleted.')
        else:
            messages.warning(request, 'Not Authorized.')
    except:
        messages.error(request, 'Comment not deleted.')
    return redirect('show_blog', b_id=cmt.blog.id)



# View a specific blog
@login_required
def show_blog(request, b_id):
    my_blog = OurBlog.objects.get(id=b_id)
    comments = Comment.objects.filter(blog__id=b_id)
    return render(request, 'general/show_blog.html', {'blog': my_blog, 'comments': comments})

# Your blogs (The logged-in user)
# From profile
@login_required
def my_blogs(request):
    # Get every blog written by the current user
    m_blogs = OurBlog.objects.filter(writer__id=request.user.id)
    return render(request, 'general/my_blogs.html', {'blogs': m_blogs})

# Create a blog
@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'general/add.html')
    elif request.method == 'POST':
        heading = request.POST['heading']
        content = request.POST['content']
        # Create the blog
        user = User.objects.get(id=request.user.id)
        OurBlog.objects.create(heading=heading, content=content, writer=user)
        messages.success(request, 'New blog added!')
        return redirect('home')
   
# Delete a blog (if you are superuser or author of the blog)
@login_required
def remove(request, b_id):
    
    try:
        my_blog = OurBlog.objects.get(id=b_id)
        if request.user.is_superuser or request.user.id==my_blog.writer.id:
            my_blog.delete()
            messages.success(request, 'Blog was successfully deleted.')
        else:
            messages.error(request, 'Not Authenticated.')
    except:
        messages.error(request, 'Blog was not deleted. Try again!')
    finally:
        return redirect('home')

# Edit a blog (if you are the author)
@login_required
def edit(request, b_id):
    # If the current user is the writer of the blog
    
        try:
            my_blog = OurBlog.objects.get(id=b_id)
        except:
            messages.error(request, 'Error occured while fetching the blog.')
            return redirect('home')
        if request.user.id==my_blog.writer.id:
            if request.method == 'GET':
                return render(request, 'general/edit.html', {'blog': my_blog})
            elif request.method == 'POST':
                content = request.POST['content']
                my_blog.content = content
                my_blog.save()
                messages.success(request, 'Blog editted successfully!')
                return redirect('home')
        else:
            messages.error(request, 'Not Authenticated.')
            return redirect('home')

# Every blog of a specific user
def user_blogs(request, b_uid):
    b_logs = OurBlog.objects.filter(writer__id=b_uid)

    return render(request, 'general/user_blogs.html', {'blogs': b_logs})


# Create a new account
def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    elif request.method == 'POST':
        uname = request.POST['username']
        passwd = request.POST['password']
        e_mail = request.POST['email']
        try:
            User.objects.create_user(username=uname, email=e_mail, password=passwd)
        except:
            messages.error(request, 'Are you kakashi? The copyusername?')
            return redirect('register')
        else:
            messages.success(request, 'Successfully created!')
            return redirect('signin')

def signin(request):
    if request.method == 'GET':
        return render(request, 'users/signin.html')
    elif request.method == 'POST':
        uname = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request, username=uname, password=passwd)
            # 'user' is not a boolen value, its a user
        if user:
            # IF user exists and is authenticated, log him/her in and return to home
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Something\'s wrong. I can feel it.')
            return redirect('signin')

# Logout
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# Your profile
@login_required
def profile(request):
    
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'GET':
        return render(request, 'users/profile.html', {'user': user})
    elif request.method == 'POST':
        uname = request.POST['username']
        new_passwd = request.POST['newpassword']
        old_passwd = request.POST['oldpassword']
        if user.check_password(old_passwd):
            if new_passwd != old_passwd and len(new_passwd) > 0 and len(uname) > 0:
                try:
                    user.username = uname
                    user.set_password(new_passwd)
                    user.save()
                    messages.success(request, 'Successfully changed')
                except:
                    messages.error(request, 'Could not change profile!')
                finally:
                    return redirect('profile')
            else:
                messages.error(request, 'Could not change profile!')
                return redirect('home')
        else:
            messages.error(request, 'Wrong password')
            return redirect('profile')

# Every single blogger
# Search function
def bloggers(request):
    every_blogger = User.objects.all()
    blog_info = []
    
    if request.method == 'GET':
        for blogger in every_blogger:
            blogger_blog = OurBlog.objects.filter(writer__id=blogger.id)
            blog_info.append( (blogger,len(blogger_blog)) )
        return render(request, 'users/bloggers.html', {'blog_info': blog_info})
    elif request.method == 'POST':
        blogger_name = request.POST['blogger_name']
        for blogger in every_blogger:
            blogger_blog = OurBlog.objects.filter(writer__id=blogger.id)
            if blogger_name.lower() in blogger.username.lower():
                blog_info.append((blogger,len(blogger_blog)))
        return render(request, 'users/bloggers.html', {"blog_info": blog_info})
