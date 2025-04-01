from django.db import models
from django.utils import timezone
import markdown
import os


class Article(models.Model):
    ARTICLE_TYPE = (
        ('article', '技术文章'),
        ('story', '原创故事'),
    )

    identifier = models.CharField(max_length=50, unique=True)  # 对应前端ID如"qqbot"
    title = models.CharField(max_length=200)
    content_md = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPE)
    date = models.DateField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)
    word_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # 自动渲染Markdown
        if self.content_md:
            self.content_html = markdown.markdown(
                self.content_md,
                extensions=[
                    'fenced_code',
                    'codehilite',
                    'tables'
                ]
            )
            self.word_count = len(self.content_md.split())
        super().save(*args, **kwargs)

    @property
    def excerpt_html(self):
        """生成摘要（前200字符）"""
        return markdown.markdown(self.content_md[:200] + "...")

    class Meta:
        ordering = ['-date']