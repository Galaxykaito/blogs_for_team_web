from django.core.management.base import BaseCommand
from articles.models import Article
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Load markdown files from directory into database'

    def handle(self, *args, **options):
        md_dir = os.path.join(settings.BASE_DIR, 'media', 'markdown')

        for filename in os.listdir(md_dir):
            if filename.endswith('.md'):
                identifier = filename[:-3]  # 移除.md后缀

                with open(os.path.join(md_dir, filename), 'r', encoding='utf-8') as f:
                    content = f.read()

                # 从内容中提取标题（假设第一行是# 标题）
                title = content.split('\n')[0].replace('#', '').strip()

                Article.objects.update_or_create(
                    identifier=identifier,
                    defaults={
                        'title': title,
                        'content_md': content,
                        'article_type': 'article' if 'articles' in filename else 'story'
                    }
                )
                self.stdout.write(f'Processed {filename}')