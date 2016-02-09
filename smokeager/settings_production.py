DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'smokeager',                       # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'autobottransform',                  # Not used with sqlite3.
        'HOST': 'localhost',                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',

    }
}

print "Settings production included!"