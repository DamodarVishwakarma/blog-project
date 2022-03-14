from django.urls import path
from blog.views import home

from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('', views.PostListView.as_view(),
         name='blog-home'),
    path('blog/create/', views.PostCreateView.as_view(),
         name='post-create'),
    path('blog/<int:pk>', views.PostDetailView.as_view(),
         name='post_detail'),
    path('blog/<int:pk>/update', views.PostUpdateView.as_view(),
         name='post-update'),
    path('blog/<int:pk>/delete', views.PostDeleteView.as_view(),
         name='post-delete'),
    path("contact/", views.contact, name="ContactUs"),
    path("about/", views.about, name="blog-about"),
]
