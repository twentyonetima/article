from django.db import models
from bs4 import BeautifulSoup
from article.script_for_models import calculate_size_of_href


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    def calculate_file_sizes(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            a_text = link.get_text()
            href = link.get('href')
            if href is not None and href[-4:] == '.iso':
                calculate_size_of_href(href, link)

        return str(soup)

class Release(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateTimeField()


class ReleaseFile(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    size = models.BigIntegerField()
    upload_date = models.DateTimeField()