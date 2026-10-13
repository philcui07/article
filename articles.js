/**
 * Article 站点 · 文章清单
 * ---------------------------------------------------------------
 * 新增一篇文章只需两步：
 *   1. 把 HTML 文件放进 posts/ 目录
 *   2. 在这个数组里追加一条记录（放在最前面即为最新）
 *
 * 字段说明：
 *   title     中文标题（必填）
 *   subtitle  英文/副标题（可选）
 *   author    作者（可选）
 *   date      发布日期 YYYY-MM-DD（用于排序与展示）
 *   tags      标签数组（可选）
 *   desc      一句话简介（可选）
 *   url       相对路径，如 posts/xxx.html（必填）
 *   badge     右上角小标记，如 中英对照 / 原创（可选）
 */
window.ARTICLES = [
  {
    title: "是什么让人类愚蠢",
    subtitle: "What Makes Humans Stupid",
    author: "David C. Krakauer",
    date: "2026-07-08",
    tags: ["译文", "AI", "复杂系统"],
    desc: "圣塔菲研究所所长克拉考尔的长文：愚蠢不是智力的缺席，而是智力的“邪恶双胞胎”——把事情错得惊天动地，恰恰需要极高的智力。全文逐段中英对照。",
    url: "posts/what-makes-humans-stupid.html",
    badge: "中英对照"
  }
  // ↓↓↓ 下一篇文章加在这里，注意上一行末尾的逗号 ↓↓↓
];
