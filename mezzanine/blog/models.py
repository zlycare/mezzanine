#encoding:utf-8
from __future__ import unicode_literals
from future.builtins import str

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from django.contrib.auth.models import User

class BlogPost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A blog post.
    """

    review_status = models.IntegerField("审核状态",
            choices=( (0, "未审核"), (1, "已审核") ), default = 0) #TODO i18n
    review_user = models.ForeignKey(User, related_name='blogpost', null=True)
    reviewed = models.DateTimeField(_("reviewed"), null=True)

    sticky_status = models.IntegerField("置顶状态",
                                        choices=((0, "未置顶"), (1, "已置顶")), default=0)  # TODO i18n
    view_count_v = models.IntegerField("虚拟阅读数",default=0,blank=True)
    like_count_v = models.IntegerField("虚拟点赞数",default=0,blank=True)

    categories = models.ManyToManyField("BlogCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="blogposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("blog.BlogPost.featured_image", "blog"),
        format="Image", max_length=255, null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("Blog post")
        verbose_name_plural = _("Blog posts")
        ordering = ("-publish_date",)
        permissions = (
            ("view_blogpost_list", "Can view blogpost list"),
        )

    def get_absolute_url(self):
        """
        URLs for blog posts can either be just their slug, or prefixed
        with a portion of the post's publish date, controlled by the
        setting ``BLOG_URLS_DATE_FORMAT``, which can contain the value
        ``year``, ``month``, or ``day``. Each of these maps to the name
        of the corresponding urlpattern, and if defined, we loop through
        each of these and build up the kwargs for the correct urlpattern.
        The order which we loop through them is important, since the
        order goes from least granular (just year) to most granular
        (year/month/day).
        """
        url_name = "blog_post_detail"
        kwargs = {"slug": self.slug}
        date_parts = ("year", "month", "day")
        if settings.BLOG_URLS_DATE_FORMAT in date_parts:
            url_name = "blog_post_detail_%s" % settings.BLOG_URLS_DATE_FORMAT
            for date_part in date_parts:
                date_value = str(getattr(self.publish_date, date_part))
                if len(date_value) == 1:
                    date_value = "0%s" % date_value
                kwargs[date_part] = date_value
                if date_part == settings.BLOG_URLS_DATE_FORMAT:
                    break
        return reverse(url_name, kwargs=kwargs)


    def save(self, *args, **kwargs):
        super(BlogPost, self).save(*args, **kwargs)




class BlogCategory(Slugged):
    """
    A category for grouping blog posts into a series.
    """

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_list_category", (), {"category": self.slug})
