AUTHOR = 'youy'
SITENAME = '悠游AI'
SITEURL = "http://localhost:8000"

PATH = "content"

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'Chinese (Simplified)'

THEME = 'themes/theme'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['sitemap', 'series','neighbors', 'related_posts']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = [
    ("我的小店", "https://m.tb.cn/h.RsjkdfC?tk=DcsDgiJeKN6/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
]

# Social widget
SOCIAL = [
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# ===== 静态文件 =====
STATIC_PATHS = ['images', 'static']
ARTICLE_EXCLUDES = ['static']         # 排除文章处理
PAGE_EXCLUDES = ['static']            # 排除页面处理

# ===== 自定义菜单 =====
MAIN_MENU = False
MENUITEMS = [
    ('打字挑战', '/static/typing-challenge.html'),
    # ('归档', '/archives.html'),
    # ('关于', '/pages/about.html'),
]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.7,   # 文章优先级高
        'indexes': 0.5,    # 分类/标签页中等
        'pages': 0.3,      # 独立页面较低
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    },
}

RELATED_POSTS_MAX = 3   # 最多显示 3 篇相关文章
