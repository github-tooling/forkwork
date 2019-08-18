# Forkwork
[![image](https://img.shields.io/pypi/v/forkwork.svg)](https://pypi.org/project/forkwork/)
[![image](https://img.shields.io/pypi/l/forkwork.svg)](https://pypi.org/project/forkwork/)
[![image](https://img.shields.io/pypi/pyversions/forkwork.svg)](https://pypi.org/project/forkwork/)

This might help to find maintained alternatives of an abandoned repo.

Inspired by [forked](https://github.com/ys/forked)   


## Requirements
* Python 3.5 and up

## Installation
from PyPI
```
$ pip install forkwork
```

from git repository
```
$ pip install git+https://github.com/github-tooling/forkwork
```

from source
```
$ git clone https://github.com/github-tooling/forkwork
$ cd forkwork
$ python setup.py install
```

## Usage

To prevent rale limit being exceeded for unauthentIcated requests, forkwork needs an access token.
For public repositories, [create a token](https://github.com/settings/tokens/new?scopes=public_repo&description=forkwork) 
with the public_repo permission.

You can use token as environment variable ``FORKWORK_TOKEN`` at ``~/.bashrc`` or ``~/.zshrc`` 

export FORKWORK_TOKEN="****************************************"

or pass token as option --token

```
$ forkwork --help
Usage: forkwork [OPTIONS] URL COMMAND [ARGS]...

Options:
  --token TEXT
  --help        Show this message and exit.

Commands:
  fnm
  top
```
top command option
```
$  forkwork https://github.com/mattdiamond/Recorderjs top --help

Usage: forkwork top [OPTIONS]

Options:
  --n INTEGER           Numbers of rows
  -S, --star            Sort by stargazers count
  -F, --forks           Sort by forks count
  -I, --open_issues     Sort by open issues count
  -D, --updated_at      Sort by updated at
  -P, --pushed_at       Sort by pushed at
  -W, --watchers_count  Sort by watchers count (Slow because requires an
                        additional request per fork)
  -C, --commits         Sort by number of commits (Slow because requires an
                        additional requests per fork)
  -B, --branches        Sort by number of branches (Slow because requires an
                        additional request per fork)
  --help                Show this message and exit.
```

### Example usage
find top repo
```
$ forkwork https://github.com/mattdiamond/Recorderjs top -S --n=5
+-----------------------------------------------+---------+---------+---------------+---------------+--------------+
| URL                                           |   Stars |   Forks |   Open Issues | Last update   | Pushed At    |
+===============================================+=========+=========+===============+===============+==============+
| https://github.com/chris-rudmin/opus-recorder |     599 |     110 |             6 | 5 days ago    | 3 months ago |
+-----------------------------------------------+---------+---------+---------------+---------------+--------------+
| https://github.com/remusnegrota/Recorderjs    |      45 |      15 |             0 | 3 months ago  | 5 years ago  |
+-----------------------------------------------+---------+---------+---------------+---------------+--------------+
| https://github.com/rokgregoric/html5record    |      41 |       7 |             0 | 9 months ago  | 7 years ago  |
+-----------------------------------------------+---------+---------+---------------+---------------+--------------+
| https://github.com/mayppong/Recorderjs        |      11 |       2 |             0 | 1 year ago    | 5 years ago  |
+-----------------------------------------------+---------+---------+---------------+---------------+--------------+
| https://github.com/jergason/Recorderjs        |      11 |      12 |             3 | 3 months ago  | 2 years ago  |
+-----------------------------------------------+---------+---------+---------------+---------------+--------------+
```

find commit that don't merged and not pushed to a pull request
```
$ forkwork https://github.com/dimka665/vk fnm

 Detrous https://github.com/Detrous/vk
1 add: proxy https://github.com/Detrous/vk/commit/87718dab306484716470fb5b1e13d7b676b1bd7b

 andriyor https://github.com/andriyor/vk
1 add support proxies
default  API version https://github.com/andriyor/vk/commit/8523ed081ea8370d7a9b6664bd8d0882ec512480
```

```
$ forkwork https://github.com/MongoEngine/eve-mongoengine fnm

 Aldream https://github.com/Aldream/eve-mongoengine
1 <attempt> Update requirements https://github.com/Aldream/eve-mongoengine/commit/3f2617b2cf978adab9296d6be9d293243d05c76e

 wdtbrno https://github.com/wdtbrno/eve-mongoengine
1 Remove autocreating where based on headers If-Modified-Since

Python-eve since 0.5 disabled If-Modified-Since on resource endpoints
Same functionality is available with
a ?where={"_udpated": {"$gt": "<RFC1123 date>"}} request. https://github.com/wdtbrno/eve-mongoengine/commit/9cb2ac3abbc210f37daff98bf5c6a3e638aeeb84
```


## Development setup
Using [Poetry](https://poetry.eustace.io/docs/)   
```
$ poetry install
```
or [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
