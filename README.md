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
└── README.md
```

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

仓库 `main` 分支根目录即站点根目录，GitHub Pages 从 **main / root** 发布。
首次需要在仓库 Settings → Pages 里把 Source 设为 `main` 分支的 `/ (root)`，之后推送即自动生效。

## 文章页样式

文章页建议自包含（内联 `<style>`），这样任何地方生成的 HTML 都能直接放进 `posts/`，不用改样式。
配色沿用本站的米白纸质风格：

| 用途 | 色值 |
| --- | --- |
| 背景 | `#fbfaf7` |
| 正文 | `#2b2b2b` |
| 强调 | `#8c3b3b` |
| 分隔线 | `#e3dfd5` |
