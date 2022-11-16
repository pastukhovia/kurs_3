import json
from json import JSONDecodeError
from main.post import Post


class PostsDAO:
    def __init__(self, posts_path, comments_path):
        self.posts_path = posts_path
        self.comments_path = comments_path

    def load_posts_from_json(self):
        '''Чтение постов из json файла'''

        try:
            with open(self.posts_path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
                posts = []

                for post in posts_data:
                    posts.append(Post(
                        post['poster_name'],
                        post['poster_avatar'],
                        post['pic'],
                        post['content'],
                        post['views_count'],
                        post['likes_count'],
                        post['pk']))

            return posts
        except JSONDecodeError as e:
            return e
        except FileNotFoundError as e:
            return e

    def load_comments_from_json(self):
        '''Чтение комментов из json файла'''

        try:
            with open(self.comments_path, 'r', encoding='utf-8') as file:
                comments = json.load(file)
            return comments
        except JSONDecodeError as e:
            return e
        except FileNotFoundError as e:
            return e

    def get_all_posts(self):
        '''Возвращает все посты'''

        return self.load_posts_from_json()

    def get_posts_by_user(self, username):
        '''Возвращает все посты указанного юзера
        args: username - имя пользователя
        returns: user_posts - список постов указанного пользователя
        '''

        posts = self.load_posts_from_json()
        user_posts = []
        if username not in [post.poster_name for post in posts]:
            raise ValueError('Пользователя с таким ником нет.')

        for post in posts:
            if post.poster_name.lower() == username.lower():
                user_posts.append(post)

        return user_posts

    def get_comments_by_post_id(self, post_id):
        '''Возвращает комменты к посту по указанному id
                args: post_id - id поста
                returns: post_comments - список комментов
        '''

        comments = self.load_comments_from_json()
        posts = self.load_posts_from_json()
        post_comments = []
        if post_id not in [post.pk for post in posts]:
            raise ValueError('Постов с таким ID нет.')

        for comment in comments:
            if comment['post_id'] == post_id:
                post_comments.append(comment)

        return post_comments

    def search_for_posts(self, query):
        '''Поиск постов по указанному запросу
                args: query - поисковой запрос
                returns: found_posts - список найденных постов
        '''

        posts = self.load_posts_from_json()
        found_posts = []

        for post in posts:
            if query.lower() in post.content.lower():
                found_posts.append(post)

        return found_posts

    def get_post_by_pk(self, pk):
        '''Возвращает пост по указанному id
                args: pk - id поста
                returns: post - найденный пост
        '''

        posts = self.load_posts_from_json()
        if pk not in [post.pk for post in posts]:
            raise ValueError('Поста с таким ID нет')

        for post in posts:
            if post.pk == pk:
                return post
