---
name: wchat-read-to-notes
description: 微信读书笔记整理为可复习、可分享的版本，做读书笔记整理时使用
---

## 处理流程
1. 用户输入的书名，简写为 book_name
1. 使用 微信读书 skill，把 book_name 对应的笔记下载到 pages-ai/book_name-读书笔记.md
2. 使用 macos 上的微信读书把插图下载到笔记中
3. check一下笔记内容下载的所有图片是否有问题，有问题重新处理一次
4. 对 pages-ai/book_name-读书笔记.md 笔记做结构化整理，去掉对阅读无用的信息，用于学习、复习、分享给大家学习，输出为 book_name-读书笔记-二次整理版.md