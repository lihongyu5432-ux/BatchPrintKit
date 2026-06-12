# 分享文案

## 短版

我做了一个开源 Windows 批量打印工具：Batch Print Kit。

它可以从资源管理器右键选中多个文件/文件夹，导入到一个打印队列里，先检查再打印。支持选择真实打印机、打开打印机驱动设置页面，PDF 会优先走 SumatraPDF，尽量避免被 WPS PDF 接管。

GitHub：
https://github.com/lihongyu5432-ux/BatchPrintKit

直接下载：
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
