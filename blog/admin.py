from django.contrib import admin
from blog.models import Post,Contact
from django.contrib.auth import get_user_model

User = get_user_model()


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at", "status")
    list_filter = ("status", "created_at", "published_at", "author")
    search_fields = ("title", "content")
    raw_id_fields = ("author",)
    date_hierarchy = "published_at"
    ordering = ("status", "-published_at")


admin.site.register(Post, PostAdmin)
admin.site.register(Contact)
