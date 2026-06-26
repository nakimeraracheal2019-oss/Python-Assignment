from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Post, Comment, PageComment
from .forms import PostForm


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        author = request.POST.get('author', 'Anonymous')
        content = request.POST.get('content', '')

        if content.strip():
            Comment.objects.create(
                post=post,
                author=author,
                content=content
            )
            return HttpResponseRedirect(request.path_info)

    comments = post.comments.all().order_by('-pub_date')
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


def home(request):
    if request.method == 'POST':
        author = request.POST.get('author', 'Anonymous')
        email = request.POST.get('email', '')
        content = request.POST.get('content', '')

        if content.strip():
            PageComment.objects.create(
                page='home',
                author=author,
                email=email,
                content=content
            )
            return HttpResponseRedirect(request.path_info)

    comments = PageComment.objects.filter(page='home').order_by('-pub_date')
    return render(request, 'blog/home.html', {'comments': comments})


def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        category = request.POST['category']
        image = request.FILES.get('image')  # ✅ handle image uploads

        Post.objects.create(
            title=title,
            body=body,
            category=category,
            image=image
        )
        return redirect('post_list')

    # ✅ this line now works for GET requests
    return render(request, 'blog/create.html')


def cyber_threats(request):
    return render(request, 'blog/threats.html')


def forensics(request):
    return render(request, 'blog/forensics.html')


def contact(request):
    return render(request, 'blog/contact.html')


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit.html', {'form': form, 'post': post})
