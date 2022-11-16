import json
from json import JSONDecodeError


def load_posts_from_json():
    try:
        with open('./data/posts.json', 'r', encoding='utf-8') as file:
            posts_data = json.load(file)
            return posts_data
    except JSONDecodeError:
        return 'Ошибка чтения JSON файла'
    except FileNotFoundError:
        return 'JSON файл не найден'


def get_post_by_pk(pk):
    posts = load_posts_from_json()

    for post in posts:
        if post['pk'] == pk:
            return post

    return f'Пост с номером {pk} не найден'

