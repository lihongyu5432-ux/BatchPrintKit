# TechRitual Submission

URL: https://startups.techritual.com/submit/

## Basic

Product name: Batch Print Kit

Tagline: 開源 Windows 批量打印工具，支援隊列檢查、右鍵導入、真實打印機選擇和 PDF 優先打印。

Website: https://lihongyu5432-ux.github.io/BatchPrintKit/

Launch year: 2026

Category: 生產力工具

Pricing: 開源

Pricing details: MIT 開源，免費使用。Windows 使用者可以直接下載 Release 壓縮包，解壓後執行 BatchPrintKit.exe；開發者也可以從 GitHub 原始碼安裝、修改和二次開發。

Platforms: Windows

Target users: 企業用戶, 一般用戶, 學生, 開發者

Tags: Windows, 批量打印, PDF, 開源, 生產力

## Product Description

Batch Print Kit 是一個專為 Windows 使用者設計的開源批量打印工具。它解決的是一個很日常但經常令人煩躁的問題：當你需要一次打印很多 PDF、Word、Excel、圖片、訂單、標籤或資料文件時，Windows 內建的右鍵打印流程很難讓人安心。文件一多，使用者很難確認最後到底會打印哪些文件；不同文件類型又會交給不同的預設應用處理；PDF 有時會被 WPS PDF 或 Microsoft Print to PDF 接管；真正的打印機設定頁面也不容易找到。

Batch Print Kit 的做法是先把文件和文件夾收集到一個可檢查的打印隊列中。使用者可以從資料夾掃描文件，也可以直接導入多個文件，或者透過 Windows Explorer 右鍵選中文件和文件夾後打開工具。所有待打印項目會先顯示在桌面介面中，包含文件名、類型、大小、打印方式和完整路徑。使用者可以在提交打印前移除不需要的文件、清空隊列、重新掃描，避免把錯誤文件送到打印機。

工具支援選擇真實打印機，並會盡量把 WPS PDF、Microsoft Print to PDF 等虛擬輸出排在實體打印機之後，降低誤選虛擬打印機的機會。桌面介面中的「打印機設定」按鈕會打開所選打印機驅動程式自己的首選項頁面，而不是跳到 Windows 系統設定首頁。這讓使用者可以直接設定紙張大小、灰度或彩色、打印品質、雙面、紙盒等由打印機驅動支援的選項。

PDF 打印方面，Batch Print Kit 可以搭配可攜式 SumatraPDF 使用。安裝腳本會下載 SumatraPDF portable，打包 Windows exe 時也可以把它放入工具目錄。這樣打印 PDF 時可以優先使用 SumatraPDF，而不是依賴 WPS 或其他預設 PDF 閱讀器，減少 PDF 被錯誤應用接管的情況。Word、Excel、PowerPoint 等 Office 文件仍會依賴 Windows 上已註冊的應用處理，這是 Windows 打印鏈路本身的限制，專案文件中也有明確說明。

Batch Print Kit 同時提供命令列工具和 Tkinter 桌面介面。CLI 保留 dry-run 機制，方便開發者或進階使用者先預覽將要打印的文件，再用明確的 `--yes` 參數提交打印。桌面介面則面向普通辦公室、倉庫、門店、學校和經常批量處理資料的人，讓不熟悉命令列的使用者也能快速操作。

專案使用 MIT License 開源，核心依賴非常少，主要使用 Python 標準庫、Tkinter 和 Windows 原生打印入口。GitHub 倉庫包含單元測試、GitHub Actions、右鍵菜單安裝腳本、Windows 11 shell extension 原始碼、Sparse Package 安裝腳本、中文 README、英文 README、使用文件和公開 issue 模板。專案目前處於早期但可用狀態，最需要的是不同 Windows 版本、不同打印機型號、不同 Office/WPS 環境下的真實兼容性回報。

## Alternatives

Windows Explorer right-click printing, WPS Office print actions, Microsoft Office manual printing, Adobe Reader / SumatraPDF single-file printing.

## Difference

Batch Print Kit 的最大差異是它不是單個文件閱讀器，也不是 Office 替代品，而是專注於「批量打印前的隊列確認和安全提交」。一般 Windows 右鍵打印會直接把選中文件交給系統處理，使用者很難在打印前再次確認隊列。Batch Print Kit 則把文件先集中到一個清楚的桌面隊列中，讓使用者在提交之前檢查、刪除和清空。

另一個差異是打印機設定入口。它不是打開 Windows 設定首頁，而是直接調用所選打印機驅動的首選項窗口，讓使用者可以設定紙張、灰度、品質和紙盒。PDF 打印方面，它也優先支援 SumatraPDF，減少 WPS PDF 或其他預設應用帶來的不確定性。

## Getting Started

第一步，從 GitHub Release 下載 BatchPrintKit-v0.2.0-win64.zip，解壓後直接運行 BatchPrintKit.exe。第二步，在桌面介面中選擇資料夾，或者點擊「導入文件」一次選中多個文件。第三步，在隊列表格中確認文件名、類型、大小和完整路徑，必要時移除選中項或清空隊列。第四步，在打印機下拉框中選擇真實打印機，點擊「打印機設定」打開打印機驅動頁面調整紙張和品質。第五步，確認隊列無誤後點擊「打印」提交任務。

進階使用者可以從 GitHub clone 原始碼，使用 `python -m pip install -e .` 安裝 CLI 和桌面入口，也可以透過 PowerShell 腳本安裝 Windows Explorer 右鍵菜單和 Send To 快捷入口。

## Extra

Project page: https://lihongyu5432-ux.github.io/BatchPrintKit/

GitHub repository: https://github.com/lihongyu5432-ux/BatchPrintKit

Latest release: https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest

Screenshot: https://lihongyu5432-ux.github.io/BatchPrintKit/images/screenshot-main.png

The project is especially looking for printer compatibility reports from real Windows users.

## Developer

Developer / company name: lihongyu5432-ux

Contact name: lihongyu5432-ux

Email: lihongyu5432-ux@users.noreply.github.com

Developer type: 個人開發者
