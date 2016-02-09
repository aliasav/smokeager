import keyring
import getpass

database_name = 'smokeager'
username = 'aliasav'
password = keyring.get_password(database_name, username)

while password == None :
    password = getpass.getpass(database_name + " Password:\n")
    # store the password
    keyring.set_password(database_name, username, password)


DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': database_name,                       # Or path to database file if using sqlite3.
        'USER': username,                      # Not used with sqlite3.
        'PASSWORD': password,                  # Not used with sqlite3.
        'HOST': 'localhost',                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',

    }
}
