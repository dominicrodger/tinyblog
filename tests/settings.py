DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'tinyblog',
)

ROOT_URLCONF = 'tests.urls'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
SECRET_KEY = 'thisbagismadefromrecycledmaterial'
ALLOWED_HOSTS = ['*']

SITE_ID = 1

TINYBLOG_FROM_EMAIL = 'from@example.com'
TINYBLOG_TITLE = 'My Blog'
TINYBLOG_AUTHORNAME = 'Bugs Bunny'
TINYBLOG_DESCRIPTION = 'Foobar'
TINYBLOG_AUTHORLINK = 'http://www.example.com'
