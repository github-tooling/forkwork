# Search by fork

This can be useful when the repository is dead and you are search for a living repository

## Installation

### Requirements
* Python 3.5 and up

### Installation from source
```
$ git clone https://github.com/andriyor/forkwork.git
$ cd forkwork
$ python3 setup.py install
```

## Usage

```
$ forkwork --help
Usage: forkwork [OPTIONS] URL

Options:
  --token TEXT
  --help        Show this message and exit.
```

### Example usage


```
$ forkwork https://github.com/dimka665/vk

 Detrous https://github.com/Detrous/vk
1 add: proxy https://github.com/Detrous/vk/commit/87718dab306484716470fb5b1e13d7b676b1bd7b

 andriyor https://github.com/andriyor/vk
1 add support proxies
default  API version https://github.com/andriyor/vk/commit/8523ed081ea8370d7a9b6664bd8d0882ec512480
```

```
$ forkwork https://github.com/MongoEngine/eve-mongoengine

 Aldream https://github.com/Aldream/eve-mongoengine
1 <attempt> Update requirements https://github.com/Aldream/eve-mongoengine/commit/3f2617b2cf978adab9296d6be9d293243d05c76e

 wdtbrno https://github.com/wdtbrno/eve-mongoengine
1 Remove autocreating where based on headers If-Modified-Since

Python-eve since 0.5 disabled If-Modified-Since on resource endpoints
Same functionality is available with
a ?where={"_udpated": {"$gt": "<RFC1123 date>"}} request. https://github.com/wdtbrno/eve-mongoengine/commit/9cb2ac3abbc210f37daff98bf5c6a3e638aeeb84
```

## Development
Install [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```