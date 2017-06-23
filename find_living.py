import getpass

from github import Github
import requests

# Authenticate to github.com and create PyGithub "Github" object
# username = input("Github Username:")
# pw = getpass.getpass()
# g = Github(username, pw)

g = Github()

url = input("Github url to repo: ")
login, repo_name = url.split('/')
repo = g.get_user(login).get_repo(repo_name)

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
