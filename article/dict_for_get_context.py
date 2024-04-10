from bs4 import BeautifulSoup

from .models import Article


import requests
from bs4 import BeautifulSoup
import time


def get_last_date():
    try:
        url = 'https://mirror.calculate-linux.org/release/'
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')
        last_el = links[-1]
        last_href = last_el.get('href')[:-1]
        return last_href
    except requests.exceptions.RequestException as e:
        return "Error fetching webpage: " + str(e)
    except (ValueError, IndexError) as e:
        return "Error processing data: " + str(e)
    except Exception as e:
        return "An unexpected error occurred: " + str(e)


def rewrite_date():
    last_href = get_last_date()

    with open("index.txt", "r") as file:
        last_id = file.read().strip()
    print("Stored ID:", last_id)

    if not last_id or int(last_id) < int(last_href):
        with open("index.txt", "w") as file:
            file.write(str(last_href))
            print("Updated ID in index.txt")
    else:
        print("No update needed.")
    return last_id


def get_new_links():
    date = rewrite_date()
    try:
        url = 'https://mirror.calculate-linux.org/release/' + date + '/'
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')
        links = [i for i in links if i.get('href') not in ['../', 'README.txt', 'SHA256SUMS.asc', 'SHA512SUMS.asc']]
        base_url = 'https://mirror.calculate-linux.org/release/' + date + '/'
        for link in links:
            href = link.get('href')
            if href and not href.startswith('http'):
                link['href'] = base_url + href
        return links
    except requests.exceptions.RequestException as e:
        return "Error fetching webpage: " + str(e)
    except (ValueError, IndexError) as e:
        return "Error processing data: " + str(e)
    except Exception as e:
        return "An unexpected error occurred: " + str(e)


def refactor_new_links():
    lst = get_new_links()
    for i in range(0, len(lst)):
        if lst[i].get_text() == 'SHA256SUMS':
            lst[i].string = 'SHA256'
        elif lst[i].get_text() == 'SHA512SUMS':
            lst[i].string = 'SHA512'
        elif lst[i].get_text().endswith('.list'):
            text_list = lst[i].get_text().split('-')
            text_list[0] = text_list[0].upper()
            lst[i].string = text_list[0] + ' list'
        elif lst[i].get_text().endswith('.iso'):
            text_lst = lst[i].get_text().split('-')
            text_lst[0] = text_lst[0].upper()
            text_lst[-1] = text_lst[-1].split('.')[0]
            text_lst.insert(0, 'Скачать')
            lst[i].string = ' '.join(text_lst)

    return lst


def create_new_dict():
    lst = refactor_new_links()
    result_dict = {}
    key = ''
    for item in lst:
        text = item.get_text()
        text_lst = text.split(' ')
        if len(text_lst) == 1:
            key = text_lst[0]
            href = item.get('href')
            result_dict[key] = f'<a href="{href}">{text}</a>'
        elif len(text_lst) == 4:
            key = text_lst[1]
            href = item.get('href')
            result_dict[key] = f'<a href="{href}">{text}</a>'
        elif len(text_lst) == 2:
            key = text
            href = item.get('href')
            result_dict[key] = f'<a href="{href}">список пакетов</a>'
    return result_dict


def res_dict():
    dct = create_dict()
    new_dict = {}

    for key, value in dct.items():
        package_name = key.split()[0]
        if package_name not in ('SHA256', 'SHA512'):
            if package_name not in new_dict:
                new_dict[package_name] = ''
            new_dict[package_name] += value + ', '

    for package_name in new_dict:
        iso_value = dct[f'{package_name} iso']
        list_value = dct[f'{package_name} list']
        new_dict[package_name] = f"{iso_value}, {dct['SHA256']}, {dct['SHA512']}, {list_value}"
    return new_dict


def create_dict():
    query = Article.objects.get(pk=1)
    article_content = query.content
    soup = BeautifulSoup(article_content, 'html.parser')
    dct = create_new_dict()
    h3_elements = soup.find_all('h3')
    print(h3_elements)
    context = dict()
    for h3 in h3_elements:
        id_element = h3.get('id')
        a_list = [''] * 4
        print(a_list)
        if id_element == 'kde_edition':
            a_list[0] = dct["CLD"]

            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLD list"]
            print(a_list)
            context['a_kde_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'cinnamon_edition':
            a_list[0] = dct["CLDC"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDC list"]
            print(a_list)
            context['a_cinnamon_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'lxqt_edition':
            a_list[0] = dct["CLDL"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDL list"]
            print(a_list)
            context['a_lxqt_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'mate_edition':
            a_list[0] = dct["CLDM"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDM list"]
            print(a_list)
            context['a_mate_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'xfce_edition':
            a_list[0] = dct["CLDX"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDX list"]
            print(a_list)
            context['a_xfce_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'scratch_edition':
            a_list[0] = dct["CLS"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLS list"]
            print(a_list)
            context['a_scratch_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'xfce_edition_scientific':
            a_list[0] = dct["CLDXS"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDXS list"]
            print(a_list)
            context['a_xfce_edition_scientific'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        else:
            print("some error")

    return context


def create_correct_dict():
    dct = create_new_dict()
    for i in range(len(dct)):
        if i == 1:
            a_list[0] = dct["CLD"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLD list"]
            print(a_list)
            context['a_kde_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'cinnamon_edition':
            a_list[0] = dct["CLDC"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDC list"]
            print(a_list)
            context['a_cinnamon_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'lxqt_edition':
            a_list[0] = dct["CLDL"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDL list"]
            print(a_list)
            context['a_lxqt_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'mate_edition':
            a_list[0] = dct["CLDM"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDM list"]
            print(a_list)
            context['a_mate_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'xfce_edition':
            a_list[0] = dct["CLDX"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDX list"]
            print(a_list)
            context['a_xfce_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'scratch_edition':
            a_list[0] = dct["CLS"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLS list"]
            print(a_list)
            context['a_scratch_edition'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)
        elif id_element == 'xfce_edition_scientific':
            a_list[0] = dct["CLDXS"]
            a_list[1] = dct["SHA256"]
            a_list[2] = dct["SHA512"]
            a_list[3] = dct["CLDXS list"]
            print(a_list)
            context['a_xfce_edition_scientific'] = ', '.join(a_list)
            a_list.clear()
            print("Clear a_list", a_list)