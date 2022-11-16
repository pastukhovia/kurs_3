import pytest
from main.posts_dao import PostsDAO
from main.post import Post

posts = PostsDAO('./data/posts.json', './data/comments.json')


def test_load_posts_from_json():
    assert type(posts.load_posts_from_json()) == list


def test_load_comments_from_json():
    assert type(posts.load_comments_from_json()) == list


def test_get_all_posts():
    assert type(posts.get_all_posts()) == list


def test_get_posts_by_user():
    with pytest.raises(ValueError):
        posts.get_posts_by_user('Oleg')
    usernames = [poster.poster_name for poster in posts.load_posts_from_json()]
    for username in usernames:
        assert type(posts.get_posts_by_user(username)) == list


def test_get_comments_by_post_id():
    with pytest.raises(ValueError):
        posts.get_comments_by_post_id(25)
    post_ids = [post.pk for post in posts.load_posts_from_json()]
    for p_id in post_ids:
        assert type(posts.get_comments_by_post_id(p_id)) == list


def test_search_for_posts():
    assert type(posts.search_for_posts('Query')) == list


def test_get_post_by_pk():
    with pytest.raises(ValueError):
        posts.get_post_by_pk(25)
    post_ids = [post.pk for post in posts.load_posts_from_json()]
    for p_id in post_ids:
        assert isinstance(posts.get_post_by_pk(p_id), Post)
