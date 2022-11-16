from flask import render_template, request, Blueprint, redirect
from main.posts_dao import PostsDAO
from main.utils import turn_hashtags_into_links, find_posts_with_tag, create_preview, add_bookmark, remove_bookmark,\
    load_bookmarks, find_bookmarked_posts


main_blueprint = Blueprint('main_blueprint', __name__, template_folder='./templates')
posts = PostsDAO('./data/posts.json', './data/comments.json')


@main_blueprint.route('/')
def index_page():
    bookmarks = load_bookmarks()
    all_posts = posts.get_all_posts()
    content_preview_list = []
    for post in all_posts:
        content_preview_list.append(create_preview(turn_hashtags_into_links(post.content), post.content))
    return render_template('index.html', posts=all_posts, content_preview=content_preview_list, bookmarks=bookmarks)


@main_blueprint.route('/posts/<int:postid>')
def post_page(postid):
    bookmarks = load_bookmarks()
    found_post = posts.get_post_by_pk(postid)
    comments = posts.get_comments_by_post_id(postid)
    content_with_hashtags = turn_hashtags_into_links(found_post.content)
    return render_template('post.html', post=found_post, comments=comments, content=content_with_hashtags,
                           bookmarks=bookmarks)


@main_blueprint.route('/search', methods=['GET'])
def search_page():
    bookmarks = load_bookmarks()
    query = request.args.get('s')
    found_posts = posts.search_for_posts(query)
    content_preview_list = []
    for post in found_posts:
        content_preview_list.append(create_preview(turn_hashtags_into_links(post.content), post.content))
    return render_template('search.html', posts=found_posts, content_preview=content_preview_list,
                           bookmarks=bookmarks)


@main_blueprint.route('/users/<username>', methods=['GET'])
def user_page(username):
    bookmarks = load_bookmarks()
    user_posts = posts.get_posts_by_user(username)
    content_preview_list = []
    for post in user_posts:
        content_preview_list.append(create_preview(turn_hashtags_into_links(post.content), post.content))
    return render_template('user-feed.html', posts=user_posts, username=username, content_preview=content_preview_list,
                           bookmarks=bookmarks)


@main_blueprint.route('/tag/<tagname>')
def tags_page(tagname):
    bookmarks = load_bookmarks()
    found_posts = find_posts_with_tag(tagname, posts.get_all_posts())
    content_preview_list = []
    for post in found_posts:
        content_preview_list.append(create_preview(turn_hashtags_into_links(post.content), post.content))
    return render_template('tag.html', posts=found_posts, tagname=tagname, content_preview=content_preview_list,
                           bookmarks=bookmarks)


@main_blueprint.route('/bookmarks/add/<int:postid>')
def add_bookmark_page(postid):
    add_bookmark(postid)
    return redirect('/', code=302)


@main_blueprint.route('/bookmarks/remove/<int:postid>')
def remove_bookmark_page(postid):
    remove_bookmark(postid)
    return redirect('/', code=302)


@main_blueprint.route('/bookmarks')
def bookmarks_page():
    bookmarks_list = load_bookmarks()
    found_posts = find_bookmarked_posts(bookmarks_list, posts.get_all_posts())
    content_preview_list = []
    for post in found_posts:
        content_preview_list.append(create_preview(turn_hashtags_into_links(post.content), post.content))
    return render_template('bookmarks.html', posts=found_posts, bookmarks=bookmarks_list,
                           content_preview=content_preview_list)
