import pytest
from api.utils import load_posts_from_json, get_post_by_pk


def test_load_posts_from_json():
    assert type(load_posts_from_json()) == list


expected_keys = ['poster_name', 'poster_avatar', 'pic',
                 'content', 'views_count', 'likes_count', 'pk']
def test_keys_in_load_posts_from_json():
    for post in load_posts_from_json():
        keys = [key for key in post.keys()]
        assert keys == expected_keys


def test_get_post_by_pk():
    for i in range(1, 8):
        assert type(get_post_by_pk(i)) == dict


expected_keys = ['poster_name', 'poster_avatar', 'pic',
                 'content', 'views_count', 'likes_count', 'pk']
def test_keys_in_get_post_by_pk():
    for i in range(1, 8):
        keys = [key for key in get_post_by_pk(i).keys()]
        assert keys == expected_keys
