from wagtail.models import Page

class HomePage(Page):
    subpage_types = ['blog.BlogIndexPage', 'blog.BlogPage']
