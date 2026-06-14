# 宣传执行清单

## 第一轮：今天就能发

1. 微信群 / 朋友圈
   - 用 `docs/share-copy.zh-CN.md` 里的“朋友圈 / 微信群”版本。
   - 配图用 `docs/images/screenshot-main.png`。
   - 目标人群：办公室、仓库、门店、学校、经常处理订单/资料的人。

2. V2EX / 开发者社区
   - 标题：`做了一个开源 Windows 批量打印工具，支持右键选中文件夹后统一打印`
   - 正文用 `V2EX / 开发者社区正文` 版本。
   - 重点说清楚：这是早期版本，欢迎真实打印机反馈。

3. GitHub
   - 确认 README 有截图、中文说明、Release 下载入口。
   - 确认 topics 已设置：`windows`, `printing`, `batch-printing`, `printer`, `desktop-app`, `python`, `pdf`。

## 第二轮：拿到反馈后再发

1. 做一个 30 秒 GIF
   - 右键选中文件
   - 打开 Batch Print Kit
   - 队列里出现文件
   - 点击打印机设置

2. 补充真实案例
   - “打印 50 个订单 PDF”
   - “打印一个资料文件夹”
   - “避免误选 WPS PDF”

3. 发英文社区
   - Reddit: Windows / productivity / opensource 相关社区
   - Hacker News: Show HN 形式
   - GitHub trending 不可控，但 README 和 topics 已经为搜索做准备

## 发布时不要这么写

- 不要说“完美适配所有打印机”。真实情况是 Windows 打印链路依赖应用和驱动。
- 不要说“完全替代 WPS/Office”。这个工具是批量队列和打印入口，不是文档渲染引擎。
- 不要承诺无人值守真实打印所有格式。PDF 比较稳，Office 文件仍依赖本机关联程序。

## 可以反复强调的真实卖点

- 打印前先检查队列
- 右键选中文件/文件夹直接导入
- 能选真实打印机
- 打印机设置打开的是驱动自己的设置页
- PDF 优先走 SumatraPDF，减少 WPS 接管问题
- 开源、MIT、可自己改
