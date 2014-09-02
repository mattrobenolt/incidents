#!/usr/bin/env python
"""
incidents
~~~~~~~~~

:copyright: (c) 2014 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

install_requires = [
    'Django>=1.7',
    'django-allauth',
    'django-jinja',
    'django-haystack',
    'celery',
    'celery-haystack',
]

tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-django',
    'flake8',
]

postgres_requires = [
    'psycopg2',
]

elasticsearch_requires = [
    'elasticsearch',
]


with open('README.rst') as f:
    long_description = f.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import sys
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='incidents',
    version='0.0.0-DEV',
    author='Matt Robenolt',
    author_email='matt@ydekproductions.com',
    url='https://github.com/mattrobenolt/incidents',
    description='',
    license='BSD',
    long_description=long_description,
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests']),
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    extras_require={
        'tests': tests_require,
        'postgres': install_requires + postgres_requires,
        'elasticsearch': install_requires + elasticsearch_requires,
    },
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'incidents = incidents.manage:main',
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
