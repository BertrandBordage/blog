#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from jinja2 import Environment as jinja2_env
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension

AUTHOR = 'Bertrand Bordage'
SITENAME = 'Bertrand Bordage'
SITESUBTITLE = 'Python libs & optimization'
SITEURL = 'http://blog.bordage.pro'

PATH = 'content'

DEFAULT_LANG = 'en'
LOCALE = 'en_US.UTF-8'
TIMEZONE = 'Europe/Paris'
DEFAULT_DATE_FORMAT = '%d %B %Y'

JINJA_EXTENSIONS = [AssetsExtension]

jinja2_env.assets_environment = AssetsEnvironment('./theme/static/', 'theme/')

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DISPLAY_CATEGORIES_ON_MENU = False

LINKS = ()

SOCIAL = (
    ('GitHub', 'https://github.com/BertrandBordage'),
    ('Gittip', 'https://www.gittip.com/BertrandBordage/'),
    ('Bitbucket', 'https://bitbucket.org/bbordage'),
    ('Facebook', 'https://www.facebook.com/bertrand.bordage'),
    ('Twitter', 'https://twitter.com/BertrandBordage'),
)
GITHUB_URL = 'https://github.com/BertrandBordage/blog'
TWITTER_USERNAME = 'BertrandBordage'


DEFAULT_PAGINATION = False

RELATIVE_URLS = True

THEME = 'theme'

ARTICLE_URL = '{slug}/'
ARTICLE_LANG_URL = '{slug}-{lang}/'
DRAFT_URL = 'drafts/{slug}/'
DRAFT_LANG_URL = 'drafts/{slug}-{lang}/'
PAGE_URL = 'pages/{slug}/'
PAGE_LANG_URL = 'pages/{slug}-{lang}/'
CATEGORY_URL = 'category/{slug}/'
TAG_URL = 'tag/{slug}/'
AUTHOR_URL = 'author/{slug}/'

ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_LANG_SAVE_AS = '{slug}-{lang}/index.html'
DRAFT_SAVE_AS = 'drafts/{slug}/index.html'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}/index.html'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}/index.html'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
TAG_SAVE_AS = 'tag/{slug}/index.html'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'

ARCHIVES_URL = 'archives/'
AUTHORS_URL = 'authors/'
CATEGORIES_URL = 'categories/'
TAGS_URL = 'tags/'

ARCHIVES_SAVE_AS = 'archives/index.html'
AUTHORS_SAVE_AS = 'authors/index.html'
CATEGORIES_SAVE_AS = 'categories/index.html'
TAGS_SAVE_AS = 'tags/index.html'

STATIC_PATHS = [
    'images',
    'CNAME',
]
