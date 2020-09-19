
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from accounts.models import User,Profile
# from tinymce import models as tinymce_models
# from accounts.models import Profile
# from tinymce.models import HTMLField

from ckeditor.fields import  RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField( unique = True,blank=True)
    discription = models.TextField()

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Blog(models.Model):
    #fields you need
    blog_views=models.IntegerField(default=0)
    # slug = models.SlugField(unique=True, blank=True)

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post2 = models.ForeignKey('post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class post(models.Model):
    statuses = [('P','Published')]
    title = models.CharField(max_length=70)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField(blank=True,null=True)
    # content = HTMLField()
    # content = models.CharField(max_length=7000)
    blog_views = models.IntegerField(default=0)
    viewed = models.IntegerField(default=0)
    status = models.CharField(max_length=1,choices=statuses)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='posts')
    image = models.ImageField(upload_to= "blog/post",blank = True)
    # date =  models.DateField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete= models.CASCADE)
    category_index = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('detail-page', kwargs={'slug':self.slug})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-date')

    @property
    def view_count(self):
        return PostView.objects.filter(post2=self).count()

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post2 = models.ForeignKey('post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


   
    