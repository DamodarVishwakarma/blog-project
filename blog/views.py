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
from .models import Post


def home(request):
    posts = Post.published.all()

    context = {
        "title": "HOME PAGE",
        "posts": posts,
    }
    return render(request, template_name="home.html", context=context)


@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'blog-home'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        posts = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(posts, self.paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_form.html'
    fields = ['title', 'contents', 'status', 'author']
    success_url = reverse_lazy('blog-home')


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'posts'
    fields = ['title', 'contents']


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView, DetailView):
    model = Post
    pk_url_kwarg = 'pk'
    template_name = 'post/post_update.html'
    context_object_name = 'posts'
    fields = ['title', 'contents', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
