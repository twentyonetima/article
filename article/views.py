import markdown
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Release, ReleaseFile
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from article.dict_for_get_context import create_dict


def release_list(request):
    releases = Release.objects.all()
    return render(request, 'release_list.html', {'releases': releases})


def release_detail(request, release_id):
    release = Release.objects.get(id=release_id)
    release_files = ReleaseFile.objects.filter(release=release)
    return render(request, 'release_detail.html', {'release': release, 'release_files': release_files})


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.content = obj.calculate_file_sizes()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dct = create_dict()
        article = self.get_object()
        article.content = article.content.replace('{{ a_kde_edition }}', dct['a_kde_edition'])
        article.content = article.content.replace('{{ a_cinnamon_edition }}', dct['a_cinnamon_edition'])
        article.content = article.content.replace('{{ a_lxqt_edition }}', dct['a_lxqt_edition'])
        article.content = article.content.replace('{{ a_mate_edition }}', dct['a_mate_edition'])
        article.content = article.content.replace('{{ a_xfce_edition }}', dct['a_xfce_edition'])
        article.content = article.content.replace('{{ a_scratch_edition }}', dct['a_scratch_edition'])
        article_content = article.content.replace('{{ a_xfce_edition_scientific }}', dct['a_xfce_edition_scientific'])

        context['article_content'] = mark_safe(article_content)
        print(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.kwargs['pk'])


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_form.html'
    fields = ['title', 'content']


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'article_form.html'
    fields = ['title', 'content', 'markdown_content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.content:
            context['markdown_content'] = markdown.markdown(self.object.content)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     article = self.get_object()
    #     soup = BeautifulSoup(article.content, 'html.parser')
    #     links = soup.find_all('a')
    #     iso_links = []
    #     for link in links:
    #         href = link.get('href')
    #         if href and href.endswith('.iso'):
    #             a_text = link.get_text()
    #             lst = a_text.split(' ')
    #             if len(lst) > 3:
    #                 iso_links.append((a_text, lst[2]))
    #             else:
    #                 iso_links.append((a_text, ''))
    #     context['iso_links'] = iso_links
    #     return context
    #
    # def form_valid(self, form):
    #     article = form.save(commit=False)
    #     article.content = self.update_iso_dates(article.content, self.request.POST)
    #     article.save()
    #     return super().form_valid(form)
    #
    # def update_iso_dates(self, content, post_data):
    #     soup = BeautifulSoup(content, 'html.parser')
    #     links = soup.find_all('a')
    #     for link in links:
    #         href = link.get('href')
    #         if href and href.endswith('.iso'):
    #             iso_link_text = link.get_text()
    #             print(f"iso_link_text: {iso_link_text}")
    #             iso_date_key = iso_link_text.strip()
    #             iso_lst_text = iso_date_key.split(' ')
    #             print(f"iso_date_key: {iso_date_key}")
    #             if iso_date_key in post_data:
    #                 if len(iso_lst_text) > 3:
    #                     new_date = post_data[iso_date_key]
    #                     print(f"new_date: {new_date}")
    #                     iso_lst_text[2] = new_date
    #                     link.string = iso_link_text.replace(iso_date_key, ' '.join(iso_lst_text), 1)
    #     return str(soup)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article_list')
