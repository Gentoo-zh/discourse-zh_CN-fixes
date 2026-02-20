Discourse 简体中文翻译修正
====

这是我用于 Arch Linux 中文论坛的修正。大部分字符串修正是通用的，但也有可能有些只适用我这个站点。

Discourse 自带的简体中文翻译有很多错漏之处，但是将之贡献给上游于我实在过于困难，翻译平台一如既往地难用。所以我把数据导出来放这儿了，要是能帮到别人就太好了。


要导入数据，请使用 `psql` 连接到数据库，然后执行：

```
\copy translation_overrides FROM '/path/to/data.csv' WITH (FORMAT CSV, HEADER);
```

Discourse Simplified Chinese translation fixes
====

This is the fixes I use for forum.archlinuxcn.org. It mostly contains fixes for general use-cases, but site-specific strings may exist too.

The Simplified Chinese translation shipped with Discourse has a lot of wrong and poor translations, but it is too hard for me to get them into upstream via the hard-to-use translation platform. So I put them here in case anyone finds it useful.

To import the data, connect to the database with `psql` and run:

```
\copy translation_overrides FROM '/path/to/data.csv' WITH (FORMAT CSV, HEADER);
```

