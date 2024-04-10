from django.test import TestCase
from django.urls import reverse
from ..models import Article
from django.contrib.auth.models import User


class ArticleUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_user.save()

        test_article = Article.objects.create(title='Test Article', content='<p>Test content</p>')
        test_article.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('article_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/articles/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('article_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('article_update', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'article_form.html')

    def test_redirects_to_detail_page_after_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('article_update', kwargs={'pk': 1}), {'title': 'Updated Title', 'content': '<p>Updated Content</p>'})
        self.assertRedirects(response, '/articles/1/')

    def test_iso_links_updated_correctly(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('article_update', kwargs={'pk': 1}), {'title': 'Test Article', 'content': '<p><a href="example.iso">ISO File</a></p>'})
        updated_article = Article.objects.get(pk=1)
        self.assertIn('<a href="example.iso">ISO File</a>', updated_article.content)
        self.assertNotIn('example.iso', updated_article.content)

