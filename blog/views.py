from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponse
from blog.models import post
from blog.forms import Contactform,Postform,Searchform,CommentForm
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView
from blog.models import Category
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count

# Create your views here.
# def index(request,*args,**kwargs):
#     posts = post.objects.filter(status = "D")
#     con = [post.title for post in posts]
#     title_str = ("\n").join(con)
#     return HttpResponse(title_str)

# def post_details(request,id,*args,**kwargs):
#     posts = post.objects.get(id=id)
#     return HttpResponse("{} \n {}".format(posts.title,posts.content))

# def index(request,*args,**kwargs):
#     posts = post.objects.all()
#     return render(request,'blog/index.html',context= {"posts":posts})

def get_category_count():
    queryset = post.objects.values('category__name').annotate(Count('category__name'))
    return queryset

class Postlistview(LoginRequiredMixin,ListView):
    login_url = 'login'
    model = post
    queryset = post.objects.filter(status="P").order_by('-date')
    # most_recent = post.objects.order_by('-date')[:3]
    paginate_by = 6
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['most_recent'] = post.objects.all().order_by('-date')[:3]
        context['category_count'] = post.objects.values('category__name').annotate(Count('category__name'))
        return context


# def post_details(request,id,*args,**kwargs):
#     posts = post.objects.get(id=id)
#     return render(request,'blog/details.html',context= {'posts':posts})

# class Postdetailview(LoginRequiredMixin,DetailView):
#     login_url = 'login'
#     model = post
#     # queryset = post.objects.filter(status="P")
#     template_name = 'blog/details.html'
#     context_object_name = 'posts'

#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         context['most_recent'] = post.objects.all().order_by('-date')[:3]
#         context['category_count'] = post.objects.values('category__name').annotate(Count('category__name'))
#         return context

def post_detail(request,slug,*args,**kwargs):
    category_count = post.objects.values('category__name').annotate(Count('category__name'))
    most_recent = post.objects.all().order_by('-date')[:3]
    post2 = get_object_or_404(post,slug=slug)
    categories = Category.objects.all()

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post2 = post2
            form.save()
            return redirect(reverse("detail-page", kwargs={
                'slug': post2.slug
            }))
    context = {
        'posts':post2,
        'most_recent':most_recent,
        'category_count':category_count,
        'categories':categories,
        'form':form,
    }
    return render(request,'blog/details.html',context)

# def contact_view(request,*args,**kwargs):
#     if request.method == "GET":
#         form = Contactform()
#         return render(request, 'blog/contact.html',context= {'form':form})
#     else:
#         print(request.POST)
#         form = Contactform(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             return HttpResponse("thank you")
#         else:
#             return  render(request, 'blog/contact.html',context= {'form':form})

class Contact_form_view(FormView):
    form_class = Contactform
    success_url = "contact"
    template_name = 'blog/contact.html'

    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)

# def post_form_view(request,*args,**kwargs):
#     if request.method == "GET":
#         form = Postform()
#         return render(request, 'blog/post.html',context={"form":form})
#     else:
#         form = Postform(request.POST,request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data.get('image').__dict__)
#             form.save()
#             return HttpResponse("Thank you")
#         return render(request, 'blog/post.html',context={"form":form})

class Post_create_view(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'login'
    permission_required = 'blog.add_post'
    form_class =  Postform
    # model = post
    # fields = ["title","content","status","category","image","date"]
    template_name = 'blog/post.html'
    # success_url = 'post'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = User.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# def edit_post_form_view(request,id,*args,**kwargs):
#     try:
#         posts = post.objects.get(id=id)
#     except:
#           return HttpResponse('invalid id')
#     if request.method == 'GET':
#         form = Postform(instance=posts)
#         return render(request,'blog/post.html',context={'form':form})
#     else:
#         form = Postform(request.POST,request.FILES,instance=posts)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('welcome')
#         else:
#             return render(request,'blog/post.html',context={'form':form})

class post_update_view(LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'login'
    permission_required = 'blog.change_post'
    model = post
    form_class = Postform
    template_name = 'blog/post.html'

    def test_func(self,*args,**kwargs):
        slug = self.kwargs.get('slug')
        posts = post.objects.get(slug = slug)
        if self.request.user.get_username()== posts.author.get_username():
            return True
        else:
            return False

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = User.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def search_view(request,*args,**kwargs):
    if request.method == 'GET':
        srch = request.GET.get('search')
        try:
            posts = post.objects.filter(title__icontains = srch)
            return render(request,'blog/search2.html',context= {"posts":posts,
                                'categories':Category.objects.all(),
                                'most_recent':post.objects.all().order_by('-date')[:3],
                                'category_count':post.objects.values('category__name').annotate(Count('category__name')),})
        except:
            return render(request,'blog/index.html',context= {"posts":posts,'categories':Category.objects.all(),
        'most_recent':post.objects.all().order_by('-date')[:3],
        'category_count':post.objects.values('category__name').annotate(Count('category__name')),})
    else:
        return render(request,'blog/index.html',context= {"posts":posts,'categories':Category.objects.all(),
        'most_recent':post.objects.all().order_by('-date')[:3],
        'category_count':post.objects.values('category__name').annotate(Count('category__name')),})

def specific_cat_list_view(request,slug,*args,**kwargs):
    cat = Category.objects.get(name__contains = slug)
    posts = cat.posts.all()
    # paginate_by = 4
    # post_list = Post.objects.all()
    paginator = Paginator(posts,6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    category_count = post.objects.values('category__name').annotate(Count('category__name'))
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'categories':Category.objects.all(),
        'most_recent':post.objects.all().order_by('-date')[:3],
        'posts':paginated_queryset,
        'page_request_var':page_request_var,
        'category_count':category_count,
    }

    if posts:
        return render(request,'blog/search.html',context)
    else:
        posts1 = post.objects.all()
        return render(request,'blog/search.html',context)

def contact_mail(request):
    if request.method == 'POST':
        message = request.POST['message']
        email = request.POST['email']
        # name = request.POST['name']
        # username = request.POST['username']

        send_mail('Approval Request (IHA Blog site)',
        message,
        settings.EMAIL_HOST_USER,
        ['nagareprathamesh07@gmail.com',email],
        fail_silently=False)

    return render(request,'blog/contact1.html')
         


