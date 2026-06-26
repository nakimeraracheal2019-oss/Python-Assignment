from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # ✅ added
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author}"


class PageComment(models.Model):
    page = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.page} comment by {self.author}"
