from urllib.parse import urlparse
from operator import attrgetter
from collections import namedtuple, OrderedDict
import calendar
from datetime import datetime, timedelta
from email.utils import parsedate, formatdate

import click
import github3
import cachecontrol
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import BaseHeuristic
from tabulate import tabulate
from halo import Halo
import pendulum


class OneDayHeuristic(BaseHeuristic):

    def update_headers(self, response):
        date = parsedate(response.headers['date'])
        expires = datetime(*date[:6]) + timedelta(days=1)
        return {
            'expires': formatdate(calendar.timegm(expires.timetuple())),
            'cache-control': 'public',
        }

    def warning(self, response):
        msg = 'Automatically cached! Response is Stale.'
        return '110 - "%s"' % msg


@click.group()
@click.argument('url')
@click.option('--token', envvar='FORKWORK_TOKEN')
@click.pass_context
def cli(ctx, url, token):
    spinner = Halo(text='Login and fetch forks', spinner='dots')
    spinner.start()

    if token:
        gh = github3.login(token=token)
    else:
        user = click.prompt('username', hide_input=False, confirmation_prompt=False)
        password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        gh = github3.login(user, password=password)
    cachecontrol.CacheControl(gh.session, cache=FileCache('.fork_work_cache'), heuristic=OneDayHeuristic())

    login, repo = urlparse(url).path[1:].split('/')
    repository = gh.repository(login, repo)
    cachecontrol.CacheControl(repository.session, cache=FileCache('.fork_work_cache'), heuristic=OneDayHeuristic())
    forks = repository.forks()

    spinner.stop()
    ctx.obj = {
        'repository': repository,
        'forks': forks,
        'gh': gh,
    }


@cli.command()
@click.pass_context
def fnm(ctx):
    repository = ctx.obj['repository']
    forks = ctx.obj['forks']

    repo_commits = repository.commits()
    cachecontrol.CacheControl(repo_commits.session, cache=FileCache('.fork_work_cache'), heuristic=OneDayHeuristic())

    repo_message = [j.message for j in repo_commits]
    old_login = ''
    for fork in forks:
        # github api may return nonexistent profile
        try:
            for c, commit in enumerate(fork.commits(), 1):
                if commit.message not in repo_message:
                    new_login = fork.owner.login
                    if old_login != fork.owner.login:
                        print('\n', new_login, fork.html_url)
                        old_login = new_login
                    click.echo(c, commit.message, commit.html_url)
        except github3.exceptions.NotFoundError:
            click.echo('Repository {} not found'.format(fork.html_url))


@cli.command()
@click.option('--n', default=10, help='Numbers of rows')
@click.option('-S', '--star', 'sort', flag_value='stargazers_count', default=True, help='Sort by stargazers count')
@click.option('-F', '--forks', 'sort', flag_value='forks_count', help='Sort by forks count')
@click.option('-I', '--open_issues', 'sort', flag_value='open_issues_count', help='Sort by open issues count')
@click.option('-D', '--updated_at', 'sort', flag_value='updated_at', help='Sort by updated at')
@click.option('-P', '--pushed_at', 'sort', flag_value='pushed_at', help='Sort by pushed at')
@click.option('-W', '--watchers_count', 'sort', flag_value='watchers', help='Sort by watchers count (Slow because requires an additional request per fork)')
@click.option('-C', '--commits', 'sort', flag_value='commits', help='Sort by number of commits (Slow because requires an additional requests per fork)')
@click.option('-B', '--branches', 'sort', flag_value='branches', help='Sort by number of branches (Slow because requires an additional request per fork)')
@click.pass_context
def top(ctx, sort, n):
    repos = []
    forks = ctx.obj['forks']
    gh = ctx.obj['gh']
    d = OrderedDict([('html_url', 'URL'), ('stargazers_count', 'Stars'), ('forks_count', 'Forks'),
                     ('open_issues_count', 'Open Issues'),
                     ('updated_at', 'Last update'), ('pushed_at', 'Pushed At')])
    headers = list(d.values())

    spinner = Halo(text='Fetch information about forks', spinner='dots')
    spinner.start()

    if sort == 'branches' or sort == 'commits' or sort == 'watchers':
        d[sort] = sort.capitalize()
        headers.append(d[sort])
        Repo = namedtuple('Repo', list(d.keys()))
    else:
        Repo = namedtuple('Repo', list(d.keys()))

    for fork in forks:
        cachecontrol.CacheControl(fork.session, cache=FileCache('.fork_work_cache'), heuristic=OneDayHeuristic())
        def_prop = [fork.html_url, fork.stargazers_count, fork.forks_count, fork.open_issues_count,
                    fork.updated_at, fork.pushed_at]
        # github api may return nonexistent profile
        if sort == 'branches':
            try:
                def_prop.append(len(list(fork.branches())))
                repos.append(Repo(*def_prop))
            except github3.exceptions.NotFoundError:
                click.echo('Repository {} not found'.format(fork.html_url))
        elif sort == 'watchers':
            try:
                repo = gh.repository(fork.owner.login, fork.name)
                def_prop.append(repo.subscribers_count)
                repos.append(Repo(*def_prop))
            except github3.exceptions.NotFoundError:
                click.echo('Repository {} not found'.format(fork.html_url))
        elif sort == 'commits':
            try:
                def_prop.append(sum([c.contributions_count for c in fork.contributors()]))
                repos.append(Repo(*def_prop))
            except github3.exceptions.NotFoundError:
                click.echo('Repository {} not found'.format(fork.html_url))
        else:
            repos.append(Repo(*def_prop))

    sorted_forks = sorted(repos, key=attrgetter(sort), reverse=True)
    humanize_dates_forks = []
    for fork in sorted_forks[:n]:
        days_passed_updated_at = (pendulum.now() - pendulum.parse(fork.updated_at)).days
        days_passed_pushed_at = (pendulum.now() - pendulum.parse(fork.pushed_at)).days
        human_updated_at = pendulum.now().subtract(days=days_passed_updated_at).diff_for_humans()
        human_pushed_at = pendulum.now().subtract(days=days_passed_pushed_at).diff_for_humans()
        humanize_dates_forks.append(fork._replace(updated_at=human_updated_at, pushed_at=human_pushed_at))

    spinner.stop()
    click.echo(tabulate(humanize_dates_forks, headers=headers, tablefmt="grid"))
