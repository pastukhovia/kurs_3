import json
from json import JSONDecodeError


def turn_hashtags_into_links(text):
    '''Преобразует теги в тексте одного поста в ссылки
    args: text - текст одного поста
    returns: output_text - текст поста с ссылками на теги в нем
    '''

    source_text = text.split()
    for i in range(len(source_text)):
        if source_text[i][0] == '#':
            source_text[i] = f'<a href="/tag/{source_text[i][1:]}">{source_text[i]}</a>'

    output_text = ' '.join(source_text)
    return output_text


def find_posts_with_tag(tagname, posts_list):
    '''Поиск постов с переданным тегом
    args: tagname - искомый хэщтег
          posts_list - список всех постов
    returns: found_posts - список найденных постов
    '''

    found_posts = []
    for post in posts_list:
        if '#' + tagname.lower() in post.content.lower():
            found_posts.append(post)

    return found_posts


def create_preview(text, text_without_links):
    '''Создание превью для постов в ленте
        args: text - текст поста с ссылками на теги в нем
              text_without_links - текст поста без ссылок
        returns: preview - сформированное превью одного поста
    '''

    # Обе версии поста преобразуются в список
    text_split = text.split()
    text_without_links_split = text_without_links.split()

    # Поиск минимального количества слов для того, чтобы отобразить необходимое количество символов в превью
    count = 0
    word_count = 0
    for word in text_without_links_split:
        if count < 50:
            count += len(word) + 1
            word_count += 1

    # Проход по тексту поста с ссылками для формирования превью с найденной ранее длиной
    i = 0
    preview = []
    while word_count > 0:
        if text_split[i] == '<a': # Если попадается начало тега ссылки, счетчик слов увеличивается,
                                  # чтобы зацепить остальную часть тега
            word_count += 1
        preview.append(text_split[i])
        i += 1
        word_count -= 1

    return ' '.join(preview)


def add_bookmark(postid):
    '''Добавление номера поста в закладки и запись в файл
            args: postid - номер поста
    '''

    new_data = {'postid': f'{postid}'}

    try:
        with open('./data/bookmarks.json', encoding='utf-8') as file:
            data = json.load(file)
            data.append(new_data)
    except JSONDecodeError as e:
        return e
    except FileNotFoundError as e:
        return e

    try:
        with open('./data/bookmarks.json', 'w', encoding='utf-8') as file1:
            json.dump(data, file1, indent=4,
                      separators=(',', ': '),
                      ensure_ascii=False)
    except JSONDecodeError as e:
        return e
    except FileNotFoundError as e:
        return e


def remove_bookmark(postid):
    '''Удаление номера поста из закладок и запись в файл
            args: postid - номер поста
    '''

    try:
        with open('./data/bookmarks.json', encoding='utf-8') as file:
            data = json.load(file)
    except JSONDecodeError as e:
        return e
    except FileNotFoundError as e:
        return e

    for i in range(len(data)):
        if int(data[i]['postid']) == postid:
            data.pop(i)
            break

    try:
        with open('./data/bookmarks.json', 'w', encoding='utf-8') as file1:
            json.dump(data, file1, indent=4,
                      separators=(',', ': '),
                      ensure_ascii=False)
    except JSONDecodeError as e:
        return e
    except FileNotFoundError as e:
        return e


def load_bookmarks():
    '''Чтение списка закладок из файла'''

    with open('./data/bookmarks.json', encoding='utf-8') as file:
        data = [int(item['postid']) for item in json.load(file)]
        return data


def find_bookmarked_posts(bm_list, posts_list):
    '''Поиск постов, которые находятся в закладках
            args: bm_list - список закладок
                  posts_list - список всех постов
            returns: found_posts - список найденных постов
    '''

    found_posts = []
    for post in posts_list:
        if post.pk in bm_list:
            found_posts.append(post)

    return found_posts
