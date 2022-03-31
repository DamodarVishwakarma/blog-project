from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
# specific to this view
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Post, Contact


def home(request):
    posts = Post.published.all()

    context = {
        "title": "HOME PAGE",
        "posts": posts,
    }
    return render(request, template_name="post/home.html", context=context)


def about(request):
    return render(request, template_name='post/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'post/contact.html')


# @method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    queryset = Post.published.all()
    model = Post
    template_name = 'post/home.html'
    ordering = ['-published_at']
    context_object_name = 'posts'
    paginate_by = 3

    # def get_context_data(self, **kwargs):
    #     context = super(PostListView, self).get_context_data(**kwargs)
    #     posts = self.get_queryset()
    #     page = self.request.GET.get('page')
    #     paginator = Paginator(posts, self.paginate_by)
    #     try:
    #         posts = paginator.page(page)
    #     except PageNotAnInteger:
    #         posts = paginator.page(1)
    #     except EmptyPage:
    #         posts = paginator.page(paginator.num_pages)
    #     context['posts'] = posts
    #     return context
    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data['title'] = "BLOG HOME PAGE"
        return context_data


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_form.html'
    fields = ['title', 'contents', 'status', 'author', 'image', 'video', 'URL_field']
    success_url = reverse_lazy('blog-home')


# @method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'posts'
    fields = ['title', 'contents', 'image', 'video', 'URL_field']


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    pk_url_kwarg = 'pk'
    template_name = 'post/post_update.html'
    context_object_name = 'posts'
    fields = ['title', 'contents', 'status', 'image', 'video', 'URL_field']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')
