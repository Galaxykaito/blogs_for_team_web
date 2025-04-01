from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def member_content(request, member_id):
    """获取成员的所有内容"""
    articles = Article.objects.filter(identifier__startswith=f'm{member_id}_article_').values(
        'identifier', 'title', 'content_html', 'date', 'views'
    )
    stories = Article.objects.filter(identifier__startswith=f'm{member_id}_story_').values(
        'identifier', 'title', 'content_html', 'date', 'word_count'
    )

    return Response({
        'articles': list(articles),
        'stories': list(stories)
    })


@api_view(['GET'])
def article_detail(request, identifier):
    """获取文章详情"""
    article = get_object_or_404(Article, identifier=identifier)
    article.views += 1
    article.save()

    return Response({
        'title': article.title,
        'content_html': article.content_html,
        'date': article.date,
        'views': article.views
    })