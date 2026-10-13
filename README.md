# Article

一个持续更新的个人文章站，托管在 GitHub Pages。

- 站点地址：https://philcui07.github.io/article/
- 目录首页：`index.html`
- 文章清单：`articles.js`

## 目录结构

```
article/
├── index.html              # 目录首页（读取 articles.js 自动渲染卡片）
├── articles.js             # 文章清单配置 ← 加文章时改这里
├── posts/                  # 文章页面存放处
│   └── what-makes-humans-stupid.html
├── site.webmanifest        # PWA 清单（「添加到桌面」图标来源）
├── favicon.ico             # 16/32/48 多尺寸
├── favicon-16/32/96/192/512.png
├── apple-touch-icon.png    # 180×180，iOS / 鸿蒙主屏图标
└── README.md
```

## 图标与「添加到桌面」

每个页面的 `<head>` 都需要带下面这组声明（首页用相对路径，文章页用 `../` 前缀）：

```html
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="96x96" href="favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#fbfaf7">
```

要点：

- **`site.webmanifest` 是鸿蒙 / 安卓「添加到桌面」取图标的主要来源**，缺了它浏览器多半会退化成默认图标或纯文字快捷方式。
- 图标必须**不透明**（无 alpha 通道），否则桌面图标可能渲染成一片空白。
- `apple-touch-icon.png` 必须 180×180，iOS 与鸿蒙都会优先读它。
- 改完图标后，用户需要**删掉旧的桌面快捷方式再重新添加**，否则会读到缓存的旧图标。

新文章页直接复制上面那段即可，把 `href` 全部加上 `../` 前缀。

## 如何新增一篇文章

两步：

1. 把你的 HTML 文件放进 `posts/`，文件名建议用英文小写 + 连字符，例如 `my-new-post.html`。
   文章页建议加上返回目录的链接：

   ```html
   <a href="../index.html">← 返回目录</a>
   ```

2. 在 `articles.js` 的数组里追加一条（**放在数组最前面即为列表首位**）：

   ```js
   {
     title: "文章标题",
     subtitle: "Subtitle / 副标题",      // 可选
     author: "作者",                      // 可选
     date: "2026-10-11",                  // 用于排序与展示
     tags: ["译文", "AI"],                 // 可选
     desc: "一句话简介。",                 // 可选
     url: "posts/my-new-post.html",
     badge: "中英对照"                     // 可选，右上角小标记
   }
   ```

然后提交推送，GitHub Pages 会自动更新：

```bash
git add .
git commit -m "add: 文章标题"
git push
```

## 部署方式

- **站点地址**：https://philcui07.github.io/article/
- 仓库 `main` 分支根目录即站点根目录，GitHub Pages 从 **main / root** 发布（已启用）

推送时二选一：

```bash
# 方式一：git 协议（需能连 github.com:443）—— 首选
GITHUB_TOKEN=ghp_xxxx ./deploy.sh

# 方式二：HTTPS API（只需能连 api.github.com）—— github.com 被墙时用它
GITHUB_TOKEN=ghp_xxxx python3 deploy_api.py
```

`deploy_api.py` 会把整个工作区打包成一个干净的 commit。注意 GitHub 的
Git Data API 不支持完全空的仓库，脚本会自动先建初始 commit。

Token 只需 **`repo`** 权限（classic token 勾 `repo` 即可）。

## 文章页样式

文章页建议自包含（内联 `<style>`），这样任何地方生成的 HTML 都能直接放进 `posts/`，不用改样式。
配色沿用本站的米白纸质风格：

| 用途 | 色值 |
| --- | --- |
| 背景 | `#fbfaf7` |
| 正文 | `#2b2b2b` |
| 强调 | `#8c3b3b` |
| 分隔线 | `#e3dfd5` |
