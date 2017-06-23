# Search by fork

This can be useful when the repository is dead and you are search for a living repository

### Example:

```
Github url to repo: dimka665/vk

 Detrous https://github.com/Detrous/vk
1 add: proxy https://github.com/Detrous/vk/commit/87718dab306484716470fb5b1e13d7b676b1bd7b

 andriyor https://github.com/andriyor/vk
1 add support proxies
default  API version https://github.com/andriyor/vk/commit/8523ed081ea8370d7a9b6664bd8d0882ec512480
```

```
Github url to repo: MongoEngine/eve-mongoengine

 Aldream https://github.com/Aldream/eve-mongoengine
1 <attempt> Update requirements https://github.com/Aldream/eve-mongoengine/commit/3f2617b2cf978adab9296d6be9d293243d05c76e

 wdtbrno https://github.com/wdtbrno/eve-mongoengine
1 Remove autocreating where based on headers If-Modified-Since

Python-eve since 0.5 disabled If-Modified-Since on resource endpoints
Same functionality is available with
a ?where={"_udpated": {"$gt": "<RFC1123 date>"}} request. https://github.com/wdtbrno/eve-mongoengine/commit/9cb2ac3abbc210f37daff98bf5c6a3e638aeeb84

 liuq https://github.com/liuq/eve-mongoengine
1 Modified eve-mongoengine dependencies. https://github.com/liuq/eve-mongoengine/commit/561057079b4f4661def2c9164d3641ee305e8d2b
2 Merge branch 'develop' of https://github.com/liuq/eve-mongoengine into develop https://github.com/liuq/eve-mongoengine/commit/1e7e5a5fea93a1542930f34bf616b701af090da6
3 Eve prescribes that by default the APIs should be read-only, therefore the default resource and item methods should just be the GET one. https://github.com/liuq/eve-mongoengine/commit/cc4c7666417489667caed8eeffcd518661d8fae0
4 According to Eve documentation, by default Eve APIs are meant to be read-only, therefore the default resource and item methods should just be GET. https://github.com/liuq/eve-mongoengine/commit/e5cf87c5623bf49958b08891c4bd838f71cb716a
5 Updated requirements to newer eve version. Tests have been performed and they successfully pass. https://github.com/liuq/eve-mongoengine/commit/a5cb12377154af382e52f9160d86efb5ebc283dc
14 Updated README for Legacy Announcement

This is the last commit of the original eve-mongoengine extension. A new
rewrite is in progress and will be released when it is ready. https://github.com/liuq/eve-mongoengine/commit/840927f264bf7ceb0505a06d620c4a6fb24cc1d3

 bumbeelabs2 https://github.com/bumbeelabs2/eve-mongoengine
1 Merge branch 'master' into develop
```

### TODO

- [ ] Get commits asynchronously
- [ ] Get number commit
- [ ] Get date commit
- [ ] Search by nested fork
- [ ] Set the depth of the search