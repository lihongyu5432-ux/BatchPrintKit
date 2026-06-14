# 分享文案

项目地址：
https://github.com/lihongyu5432-ux/BatchPrintKit

直接下载：
https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest

## 短版

我做了一个开源 Windows 批量打印工具：Batch Print Kit。

它可以从资源管理器右键选中多个文件/文件夹，导入到一个打印队列里，先检查再打印。支持选择真实打印机、打开打印机驱动设置页面，PDF 会优先走 SumatraPDF，尽量避免被 WPS PDF 接管。

GitHub：
https://github.com/lihongyu5432-ux/BatchPrintKit

直接下载：
https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest

## 朋友圈 / 微信群

做了个 Windows 小工具，叫 Batch Print Kit，解决一个很具体但挺烦的问题：批量打印。

平时如果要打印一堆 PDF、Excel、Word、图片，Windows 右键打印很容易失控：不知道到底选了哪些文件，PDF 还可能被 WPS 接管，打印机设置也绕来绕去。

这个工具的思路比较简单：

- 先把文件/文件夹导入到队列
- 打印前能检查、删除、清空
- 可以选择真实打印机
- 能打开打印机自己的设置页面
- PDF 优先用 SumatraPDF 打印
- 支持资源管理器右键打开

开源地址：
https://github.com/lihongyu5432-ux/BatchPrintKit

如果你经常给订单、资料、表格、标签批量打印，可以试试。

## 小红书 / 即刻 / 朋友圈短帖

Windows 批量打印真的很麻烦。

我做了一个开源小工具：Batch Print Kit。

它不是复杂软件，就是把一堆文件先放到打印队列里，让你确认清楚后再打印。支持右键导入文件/文件夹、选择真实打印机、打开打印机驱动设置，PDF 优先走 SumatraPDF，避免被 WPS PDF 接管。

适合办公室、仓库、门店、学校资料打印。

GitHub 搜 BatchPrintKit，或者直接看：
https://github.com/lihongyu5432-ux/BatchPrintKit

## V2EX / 吾爱破解 / 开发者社区标题

- 做了一个开源 Windows 批量打印工具，支持右键选中文件夹后统一打印
- 分享一个自己做的 Windows 批量打印工具：Batch Print Kit
- Windows 批量打印 PDF/Excel/图片太麻烦，我做了个开源小工具

## V2EX / 开发者社区正文

最近做了一个很小的 Windows 工具：Batch Print Kit。

起因是实际工作里经常要批量打印资料、表格、订单、PDF、图片。Windows 自带右键打印对单个文件还行，但文件一多就很难确认队列，也容易被 WPS PDF / Microsoft Print to PDF 这类虚拟打印机带偏。

这个工具目前做了这些：

- Tkinter 桌面界面
- 支持扫描文件夹和导入多个文件
- 打印前显示完整队列，可以移除单项或清空
- 支持选择打印机
- `打印机设置` 会打开选中打印机的驱动首选项窗口
- PDF 优先使用 SumatraPDF
- 支持 Windows 右键菜单 / Send To
- CLI 仍保留 dry-run 机制，防止误打印
- MIT 开源

项目地址：
https://github.com/lihongyu5432-ux/BatchPrintKit

Release 里有 Windows zip，解压后直接运行 `BatchPrintKit.exe`。

目前还是早期版本，主要想先把“可靠地批量打印”这件事做好。如果你有真实打印机环境，欢迎试用、提 issue，尤其欢迎反馈不同打印机/WPS/Office 环境下的兼容性。

## GitHub / Reddit / Hacker News 英文短帖

I built Batch Print Kit, a small open-source Windows tool for batch printing.

The goal is simple: select many files or folders, review the exact print queue, choose the real printer, open the printer driver's own preferences page, and then print. PDFs can go through bundled SumatraPDF so they do not accidentally get routed through WPS PDF or another default PDF handler.

It includes a Tkinter desktop UI, a CLI, Windows Explorer integration scripts, tests, and an MIT license.

GitHub:
https://github.com/lihongyu5432-ux/BatchPrintKit

Windows download:
https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest

## 长版

Windows 批量打印一堆 PDF、表格、图片、资料文件时，经常会遇到几个问题：选中的文件太多不好确认、PDF 被 WPS 接管、打印机设置不好找、右键打印行为不稳定。

所以我做了一个小工具 Batch Print Kit：

- 支持文件夹扫描和多文件导入
- 打印前显示完整队列，可以移除不想打印的文件
- 可以选择真实打印机
- `打印机设置` 会打开打印机驱动自己的设置界面
- PDF 优先使用 SumatraPDF 打印
- 支持 Windows 右键菜单
- MIT 开源

目前是早期版本，欢迎试用、提 issue、点 star。

## 英文长版

Batch Print Kit is a small open-source Windows batch printing tool.

It is built for a boring but common workflow: printing a pile of PDFs, spreadsheets, documents, images, labels, or order files without losing track of what is being sent to the printer.

What it does:

- scan folders and collect printable files
- import many files directly
- review and clean the queue before printing
- choose a real printer from the desktop app
- open the selected printer driver's own preferences window
- print PDFs through optional bundled SumatraPDF
- add Windows Explorer context-menu integration
- keep a CLI dry-run path for safer automation

Repository:
https://github.com/lihongyu5432-ux/BatchPrintKit

Download:
https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest

Feedback from real printer setups is welcome.
