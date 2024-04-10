# update_article_content.py

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from article.models import Article


class Command(BaseCommand):
    help = 'Modifies and saves the content field of the article with id = 2'

    def handle(self, *args, **options):
        # Fetch the article with id = 2 or raise a 404 error if not found
        article = Article.objects.get(id=2)

        # Print the original content
        self.stdout.write(f'Original Content: {article.content}')
#         # Update the content field with the desired HTML content
#         article.content = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Title</title>
# </head>
# <body>
#
# </body>
# </html>
# """
#         # Save the changes
#         article.save()
#
#         self.stdout.write(self.style.SUCCESS('Successfully updated article content.'))
