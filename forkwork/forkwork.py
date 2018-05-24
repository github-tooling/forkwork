from urllib.parse import urlparse

import click
from tqdm import tqdm
from github import Github
import requests

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    pass


@click.command()
@click.argument('url')
@click.option('--token', envvar='FORKWORK_TOKEN')
def cli(url, token):
    if token:
        g = Github(token)
    else:
        user = click.prompt('username', hide_input=False, confirmation_prompt=False)
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        g = Github(user, password)

    login, repo = urlparse(url).path[1:].split('/')
    repo = g.get_user(login).get_repo(repo)

    repo_commits = repo.get_commits()
    repo_message = [j.commit.message for j in repo_commits]
    forks = repo.get_forks()
    old_login = ''

    for fork in forks:
        if requests.get(fork.html_url).status_code != 404:
            for c, commit in enumerate(fork.get_commits(), 1):
                if commit.commit.message not in repo_message:
                    new_login = fork.owner.login
                    if old_login != fork.owner.login:
                        print('\n', new_login, fork.html_url)
                        old_login = new_login
                    print(c, commit.commit.message, commit.commit.html_url)
