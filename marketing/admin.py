from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "is_published", "created_at", "created_by")
    list_filter = ("type", "is_published")
    search_fields = ("title", "content")
