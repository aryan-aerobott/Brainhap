from django.http import JsonResponse
from blog.models import BlogPage


def blog_detail_api(request, slug):
    try:
        blog = BlogPage.objects.live().public().get(slug=slug)

        return JsonResponse({
            "id": blog.id,
            "title": blog.title,
            "slug": blog.slug,
            "published_at": blog.first_published_at,
            "body_html": blog.body,   # ✅ THIS IS CORRECT
            "categories": [c.name for c in blog.categories.all()],
            "url": blog.url,
        })

    except BlogPage.DoesNotExist:
        return JsonResponse(
            {"error": "Blog not found"},
            status=404
        )
