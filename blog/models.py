from django.db import models
from rest_framework import serializers

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField

from django.core.paginator import Paginator
from modelcluster.fields import ParentalManyToManyField


# ---------------------------
# Blog Category (Snippet)
# ---------------------------
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"


# ---------------------------
# Blog Index Page
# ---------------------------
class BlogIndexPage(Page):
    subpage_types = ["blog.BlogPage"]

    def get_context(self, request):
        context = super().get_context(request)

        # Only show blogs under THIS index page
        blogs = BlogPage.objects.child_of(self).live().public().order_by("-first_published_at")

        # Pagination
        paginator = Paginator(blogs, 6)
        page = request.GET.get("page")
        blogs = paginator.get_page(page)

        context["blogs"] = blogs
        return context


# ---------------------------
# Blog Page
# ---------------------------
class BlogPage(Page):

    date = models.DateField("Post date", null=True, blank=True)

    intro = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    body = RichTextField(blank=True)

    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    categories = ParentalManyToManyField(
        "blog.BlogCategory",
        blank=True,
        related_name="blog_pages"
    )

    def author(self):
        return self.owner.get_full_name() or self.owner.username

    @property
    def rendered_body(self):
        from wagtail.rich_text import expand_db_html
        return expand_db_html(self.body)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("feed_image"),
        FieldPanel("categories"),
    ]

    api_fields = [
        APIField("date"),
        APIField("intro"),
        APIField("body", serializer=serializers.CharField(source="rendered_body")),
        APIField("feed_image", serializer=ImageRenditionField("original")),
        APIField("author"),
        APIField("categories"),
    ]