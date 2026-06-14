# Launch Posts

## Hacker News

Source guideline notes:

- Show HN is for something you made that people can try.
- The title should begin with `Show HN`.
- Make it easy to try without signup.
- Do not ask for upvotes.

Title:

```text
Show HN: Batch Print Kit – an open-source Windows batch printing tool
```

URL:

```text
https://lihongyu5432-ux.github.io/BatchPrintKit/
```

Optional first comment:

```text
I built this after running into a boring Windows workflow problem: printing a mixed folder of PDFs, spreadsheets, documents, and images is awkward once you need to review the queue first.

Batch Print Kit is a small Tkinter desktop app plus CLI. It lets you import files/folders, review the queue, choose a real printer, open the selected printer driver's preferences page, and print PDFs through bundled SumatraPDF when installed.

It is early, MIT licensed, and feedback from real Windows printer setups would be especially useful.
```

Submit page:

```text
https://news.ycombinator.com/submit
```

## Product Hunt

Product name:

```text
Batch Print Kit
```

Tagline:

```text
Open-source Windows batch printing with queue review and Explorer integration.
```

Website:

```text
https://lihongyu5432-ux.github.io/BatchPrintKit/
```

Description:

```text
Batch Print Kit is a small open-source Windows desktop tool for printing folders of PDFs, Office documents, images, labels, and order files without losing track of the queue.

Select files or folders from Explorer, review the exact print queue, choose the real printer, open the printer driver's own preferences page, and print. PDFs can use bundled SumatraPDF to reduce accidental routing through WPS PDF or another default PDF handler.
```

First maker comment:

```text
Hi Product Hunt, I made Batch Print Kit for a very ordinary Windows workflow: printing a mixed pile of files without accidentally sending the wrong thing to the wrong printer.

It is open source, MIT licensed, and intentionally small. The current version includes a Tkinter desktop UI, CLI, Windows Explorer integration scripts, optional SumatraPDF PDF printing, and unit tests.

I would love feedback from people with real printer setups, especially around printer-driver compatibility and Office/WPS environments.
```

Suggested gallery assets:

- `docs/images/screenshot-main.png`
- 30 second GIF: right-click files, open app, review queue, open printer settings
- Screenshot of GitHub Release download page

Submit page:

```text
https://www.producthunt.com/posts/new
```

## Reddit r/opensource

Important rule notes:

- Use the correct `Promotional` flair.
- Avoid excessive self-promotion.
- Engage in the comments instead of drive-by posting.
- The linked repo must have an OSI open-source license.

Title:

```text
I built an open-source Windows batch printing tool
```

Body:

```text
I built Batch Print Kit, a small MIT-licensed Windows tool for batch printing.

It is meant for a boring workflow: printing a folder of PDFs, spreadsheets, documents, images, labels, or order files while still being able to review the queue first.

Current features:

- Tkinter desktop UI
- multi-file import and folder scan
- queue review before printing
- printer selection
- opens the selected printer driver's own settings page
- optional SumatraPDF backend for PDFs
- Windows Explorer integration scripts
- CLI with dry-run behavior

GitHub:
https://github.com/lihongyu5432-ux/BatchPrintKit

I would especially appreciate real printer compatibility reports.
```

## Chinese Communities

Title:

```text
做了一个开源 Windows 批量打印工具，支持右键选中文件夹后统一打印
```

Body:

```text
最近做了一个很小的 Windows 工具：Batch Print Kit。

起因是实际工作里经常要批量打印资料、表格、订单、PDF、图片。Windows 自带右键打印对单个文件还行，但文件一多就很难确认队列，也容易被 WPS PDF / Microsoft Print to PDF 这类虚拟打印机带偏。

这个工具目前做了这些：

- Tkinter 桌面界面
- 支持扫描文件夹和导入多个文件
- 打印前显示完整队列，可以移除单项或清空
- 支持选择打印机
- 打印机设置会打开选中打印机的驱动首选项窗口
- PDF 优先使用 SumatraPDF
- 支持 Windows 右键菜单 / Send To
- CLI 保留 dry-run 机制，防止误打印
- MIT 开源

项目地址：
https://github.com/lihongyu5432-ux/BatchPrintKit

Release 里有 Windows zip，解压后直接运行 BatchPrintKit.exe。

目前还是早期版本，主要想先把“可靠地批量打印”这件事做好。如果你有真实打印机环境，欢迎试用、提 issue，尤其欢迎反馈不同打印机/WPS/Office 环境下的兼容性。
```
