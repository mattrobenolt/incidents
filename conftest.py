def pytest_report_header(config):
    return 'made with love: <3'


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        DATABASE_ENGINE='sqlite3',
        DATABASES={
            'default': {
                'NAME': ':memory:',
                'ENGINE': 'django.db.backends.sqlite3',
                'TEST_NAME': ':memory:',
            },
        },
        PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'],
    )
