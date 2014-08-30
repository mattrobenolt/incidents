from invoke import run as _run, task
from functools import partial

# Always echo out commands
run = partial(_run, echo=True, pty=True)


@task
def lint(verbose=False):
    "Run flake8 linter"
    run('flake8 src/incidents tests *.py {0}'.format('-v' if verbose else ''))


@task(lint)
def test(verbose=False):
    "Run tests using py.test"
    run('py.test --cov incidents --cov-report term-missing {0}'.format('-v' if verbose else ''))


@task
def clean():
    "Clean working directory"
    run('rm -rf **/*.egg-info **/*.egg **/*.pyc dist build')
