#coding:utf-8
from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogPost, BlogCategory, Area
from mezzanine.conf import settings
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.twitter.admin import TweetableAdminMixin

blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
#XXX blogpost_fieldsets[0][1]["fields"].insert(1, "categories")
# 参考core/admin.py中DispalyableAdmin的fieldsets
blogpost_fieldsets[0][1]["fields"].extend(["source_name"]) #显示来源字段
blogpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])
#XXX blogpost_fieldsets[0][1]["fields"].extend(["keywords"]) #放在上面编辑保存无效，暂时放回MetaData
blogpost_fieldsets[0][1]["fields"].extend(["categories"])


blogpost_list_display = ["title", "user", "status", "review_status", "sticky_status", "admin_link"]
if settings.BLOG_USE_FEATURED_IMAGE:
    blogpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    blogpost_list_display.insert(0, "admin_thumb")
blogpost_fieldsets = list(blogpost_fieldsets)
#XXX blogpost_fieldsets.insert(1, (_("Other posts"), {
#XXX     "classes": ("collapse-closed",),
#XXX     "fields": ("related_posts",)}))
blogpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("user","categories","review_status","sticky_status","source_name")


class BlogPostAdmin(TweetableAdminMixin, DisplayableAdmin, OwnableAdmin):
    """
    Admin class for blog posts.
    """

    fieldsets = fieldsets_original = blogpost_fieldsets
    list_display = blogpost_list_display
    list_filter = blogpost_list_filter
    filter_horizontal = ("categories", "areas", "content_categories","form_categories" )

    addon_fieldsets = [(_("运营调整"), {
        "fields": [("review_status", "sticky_status"),
                   ("view_count_v", "like_count_v"),
                   "grade", "content_categories", "form_categories"],
        "classes": ("collapse-open",)
    })]
    manage_fieldsets = fieldsets + addon_fieldsets
    addnewblog_fieldsets = fieldsets[:-1]

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        self.save_reviewer_form(form, request)
        return DisplayableAdmin.save_form(self, request, form, change)

    def get_form(self, request, obj=None, *args, **kwargs):
        if obj:
            # 修改文章
            if request.user.has_perm('blog.edit_operational_fields'):
                self.fieldsets = self.manage_fieldsets
            else:
                self.fieldsets = self.fieldsets_original
                self.readonly_fields = ('_meta_title', 'slug', 'publish_date','expiry_date')
        else:
            # 新增文章
            if request.user.has_perm('blog.edit_operational_fields'):
                self.fieldsets = self.manage_fieldsets
            else:
                self.fieldsets = self.addnewblog_fieldsets
                self.readonly_fields = ('publish_date','expiry_date')

        form = super(BlogPostAdmin, self).get_form(request, *args, **kwargs)
        form.request = request
        return form

    def save_related(self, request, form, *args, **kwargs):
        super(BlogPostAdmin, self).save_related(request, form, *args, **kwargs)

    def save_reviewer_form(self, form, request):
        obj = form.save(commit=False)
        review_ok = 1
        from django.utils import timezone
        if obj.review_status == review_ok and obj.review_user is None:
            obj.review_user = request.user
            obj.reviewed = timezone.now()


    # 使用Django的信号机制，在文章保存后生成关键词和分类
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    @receiver(post_save, sender=BlogPost)
    def blogpost_after(sender, created, instance, **kwargs):
        blogpost = instance
        if (blogpost.id):
            from mezzanine.blog import api_zmq
            # api_zmq.auto_gen_keywords_message(blogpost.id, blogpost.content)
            api_zmq.auto_gen_category_message(blogpost.id, blogpost.content)
            api_zmq.auto_gen_search_index_message(blogpost.id, blogpost.content)

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


# class AreaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'name', 'parent', 'level')
#
#
# admin.site.register(Area, AreaAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
