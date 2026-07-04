# Discourse 简繁中文翻译修正

fork 自 lilydjwg/discourse-zh_CN-fixes，在他的简体修正之上补齐正体中文和一批更正。

`data.csv` 是 lilydjwg 的原文件，一字没动，跟着上游走。`data-supplement.csv` 是这个 fork 加的：正体中文译文（台湾用词，档案、软体、预设、登入这些），以及一批 stock 错译的更正。stock 正体有不少实打实的错，比如把「你的暱称」当全名、「两小时内」当「两小时后」、「寄出密码」当「重设密码」；界面上也有 liked 译成 linked、「信息」和「消息」不分、「投票结果已公布」其实是「投票额度已释放」这类。补充里大部分是通用的 Discourse 修正，能贡献回上游；少数几条是本站专属，比如 Codeberg 登录按钮的文案。

## 导入

两份都用 `psql` 导进 `translation_overrides` 表：

```
\copy translation_overrides FROM 'data.csv' WITH (FORMAT CSV, HEADER)
\copy translation_overrides FROM 'data-supplement.csv' WITH (FORMAT CSV, HEADER)
```

两份的 `(locale, translation_key)` 不重叠，先后导入不冲突。导过旧版的先清掉再导：

```
DELETE FROM translation_overrides WHERE locale IN ('zh_CN', 'zh_TW');
```

直接写表绕过了模型回调，导入后重启一次 Discourse，前端才拿得到新译文。

信任级别自动组的名字（trust_level_0～4）是存在组的 `full_name` 字段里的静态值，光导入翻译不会改到已有的组，还要跑一次刷新：

```
docker exec app rails runner 'Group.refresh_automatic_groups!'
```

## 文件

`data.csv` 是 lilydjwg 的简体修正，原样保留，`git pull upstream` 能干净合并他的更新。`data-supplement.csv` 是本项目补充的正体和更正，列跟 `data.csv` 一样：`locale, translation_key, value, created_at, updated_at, original_translation, status`。

## 来源

简体底本是 lilydjwg 为 archlinuxcn 论坛维护的 discourse-zh_CN-fixes，本仓库是它的 fork，正体和补全为 Gentoo-zh 社区所加。上游未附许可证。
