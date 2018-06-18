from urllib.parse import urlparse
from operator import attrgetter
from collections import namedtuple

import click
import requests
import github3
import cachecontrol
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import BaseHeuristic
from tabulate import tabulate

try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    pass


class OneWeekHeuristic(BaseHeuristic):
    def update_headers(self, response):
        seconds_in_week = 604800
        return {'Cache-Control': f'private, max-age={seconds_in_week}, s-maxage={seconds_in_week}'}


@click.group()
@click.argument('url')
@click.option('--token', envvar='FORKWORK_TOKEN')
@click.pass_context
def cli(ctx, url, token):
    if token:
        gh = github3.login(token=token)
    else:
        user = click.prompt('username', hide_input=False, confirmation_prompt=False)
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        gh = github3.login(user, password=password)
    cachecontrol.CacheControl(gh.session, cache=FileCache('.fork_work_cache'), heuristic=OneWeekHeuristic())

    login, repo = urlparse(url).path[1:].split('/')
    repository = gh.repository(login, repo)
    cachecontrol.CacheControl(repository.session, cache=FileCache('.fork_work_cache'), heuristic=OneWeekHeuristic())
    forks = repository.forks()

    ctx.obj = {
        'repository': repository,
        'forks': forks,
    }


@cli.command()
@click.pass_context
def fnm(ctx):
    repository = ctx.obj['repository']
    forks = ctx.obj['forks']

    repo_commits = repository.commits()
    cachecontrol.CacheControl(repo_commits.session, cache=FileCache('.fork_work_cache'), heuristic=OneWeekHeuristic())

    repo_message = [j.message for j in repo_commits]
    old_login = ''
    for fork in forks:
        if requests.get(fork.html_url).status_code != 404:
            for c, commit in enumerate(fork.commits(), 1):
                if commit.message not in repo_message:
                    new_login = fork.owner.login
                    if old_login != fork.owner.login:
                        print('\n', new_login, fork.html_url)
                        old_login = new_login
                    print(c, commit.message, commit.html_url)


@cli.command()
@click.option('--n', default=10, help='Numbers of rows')
@click.option('-S', '--star', 'sort', flag_value='stargazers_count', default=True, help='Sort by stargazers count')
@click.option('-F', '--forks', 'sort', flag_value='forks_count', help='Sort by forks count')
@click.option('-I', '--open_issues', 'sort', flag_value='open_issues_count', help='Sort by open issues count')
@click.option('-D', '--updated_at', 'sort', flag_value='updated_at', help='Sort by updated at')
@click.pass_context
def top(ctx, sort, n):
    repos = []
    forks = ctx.obj['forks']
    Repo = namedtuple('Repo', ['html_url', 'stargazers_count', 'forks_count', 'open_issues_count', 'updated_at'])

    for f in forks:
        cachecontrol.CacheControl(f.session, cache=FileCache('.fork_work_cache'), heuristic=OneWeekHeuristic())
        repos.append(Repo(f.html_url, f.stargazers_count, f.forks_count, f.open_issues_count, f.updated_at))
    sorted_repos = sorted(repos, key=attrgetter(sort), reverse=True)

    headers = ['URL', 'Stars', 'Forks', 'Open Issues', 'Last update']
    print(tabulate(sorted_repos[:n], headers=headers, tablefmt="grid"))
