from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm
from accounts.forms import Signupform
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,View
from accounts.forms import UserEditForm,ProfileEditForm
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from blog.models import post
from django.views.generic import ListView
from blog.models import Category
from django.db.models import Count

# Create your views here.
class Signup_create_view(CreateView):
    form_class = Signupform
    template_name = 'account/signup.html'
    success_url = '/blog'


# class HomePageView(TemplateView):
#     template_name = 'account/home.html'
#     model = post
#     context_object_name = 'posts'

#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context['most_recent'] = post.objects.all().order_by('-date')[:3]
#         return context

class Postlistview(ListView):
    # login_url = 'login'
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
        context['categories_index'] = post.objects.all()
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'


class ProfileUpdateView(LoginRequiredMixin,View):
    login_url = 'login'

    def get(self,request):
        print('GETTING HERE')
        u_form = UserEditForm(instance= request.user)
        p_form = ProfileEditForm(instance= request.user.profile)

        context = { 
            'u_form':u_form,
            'p_form':p_form
        }
        return render(request, 'account/profile_update.html',context)

    def post(self,request):
        u_form = UserEditForm(request.POST,instance= request.user)
        p_form = ProfileEditForm(request.POST,request.FILES,instance= request.user.profile)

        context = { 
            'u_form':u_form,
            'p_form':p_form
        }

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return render(request, 'account/profile.html',context)