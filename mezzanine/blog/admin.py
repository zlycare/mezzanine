#coding:utf-8
from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.conf import settings
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.twitter.admin import TweetableAdminMixin

blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
#XXX blogpost_fieldsets[0][1]["fields"].insert(1, "categories")
blogpost_fieldsets[0][1]["fields"].extend(["review_status"]) #显示审核状态
blogpost_fieldsets[0][1]["fields"].extend(["source_name"]) #显示来源字段
blogpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])
#XXX blogpost_fieldsets[0][1]["fields"].extend(["keywords"]) #放在上面编辑保存无效，暂时放回MetaData
blogpost_fieldsets[0][1]["fields"].extend(["categories"])

blogpost_list_display = ["title", "user", "status", "review_status", "admin_link"]
if settings.BLOG_USE_FEATURED_IMAGE:
    blogpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    blogpost_list_display.insert(0, "admin_thumb")
blogpost_fieldsets = list(blogpost_fieldsets)
#XXX blogpost_fieldsets.insert(1, (_("Other posts"), {
#XXX     "classes": ("collapse-closed",),
#XXX     "fields": ("related_posts",)}))
blogpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories","review_status",)


class BlogPostAdmin(TweetableAdminMixin, DisplayableAdmin, OwnableAdmin):
    """
    Admin class for blog posts.
    """

    fieldsets = blogpost_fieldsets
    list_display = blogpost_list_display
    list_filter = blogpost_list_filter
    filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)

    def save_related(self, request, form, *args, **kwargs):
        super(BlogPostAdmin, self).save_related(request, form, *args, **kwargs)

        blogpost = form.instance
        blogpost.autogen_ifnot_category()

class BlogCategoryAdmin(BaseTranslationModelAdmin):
    """
    Admin class for blog categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def has_module_permission(self, request):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "blog.BlogCategory" in items:
                return True
        return False


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
