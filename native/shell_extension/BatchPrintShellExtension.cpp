#include <windows.h>
#include <shobjidl.h>
#include <strsafe.h>

#include <string>
#include <vector>
#include <new>

// Thin Windows Explorer command handler. It only gathers selected filesystem
// paths and launches the existing BatchPrintKit.exe. Keep Explorer-hosted code
// small; the Python/Tk app owns the real UI and print workflow.

static const CLSID CLSID_BatchPrintExplorerCommand =
    {0x61f77b19, 0xaf18, 0x4f36, {0x90, 0x58, 0x6f, 0x9d, 0xe5, 0x0e, 0x59, 0x31}};

static long g_lockCount = 0;
static long g_objectCount = 0;
static HMODULE g_module = nullptr;

static std::wstring DuplicateString(const wchar_t* value) {
    return value ? std::wstring(value) : std::wstring();
}

static HRESULT AllocShellString(const std::wstring& value, PWSTR* result) {
    if (!result) {
        return E_POINTER;
    }
    const size_t bytes = (value.size() + 1) * sizeof(wchar_t);
    *result = static_cast<PWSTR>(CoTaskMemAlloc(bytes));
    if (!*result) {
        return E_OUTOFMEMORY;
    }
    HRESULT hr = StringCchCopyW(*result, value.size() + 1, value.c_str());
    if (FAILED(hr)) {
        CoTaskMemFree(*result);
        *result = nullptr;
    }
    return hr;
}

static std::wstring QuoteArg(const std::wstring& arg) {
    std::wstring quoted = L"\"";
    for (wchar_t ch : arg) {
        if (ch == L'"') {
            quoted += L"\\\"";
        } else {
            quoted += ch;
        }
    }
    quoted += L"\"";
    return quoted;
}

static std::wstring ReadAppPath() {
    wchar_t buffer[MAX_PATH * 4] = {};
    DWORD bufferBytes = sizeof(buffer);
    LSTATUS status = RegGetValueW(
        HKEY_CURRENT_USER,
        L"Software\\BatchPrintKit",
        L"AppPath",
        RRF_RT_REG_SZ,
        nullptr,
        buffer,
        &bufferBytes);
    if (status == ERROR_SUCCESS && buffer[0] != L'\0') {
        return DuplicateString(buffer);
    }
    return std::wstring();
}

static HRESULT LaunchBatchPrintKit(IShellItemArray* items) {
    if (!items) {
        return E_INVALIDARG;
    }

    std::wstring appPath = ReadAppPath();
    if (appPath.empty()) {
        return HRESULT_FROM_WIN32(ERROR_FILE_NOT_FOUND);
    }

    DWORD count = 0;
    HRESULT hr = items->GetCount(&count);
    if (FAILED(hr)) {
        return hr;
    }

    std::wstring commandLine = QuoteArg(appPath);
    for (DWORD index = 0; index < count; ++index) {
        IShellItem* item = nullptr;
        hr = items->GetItemAt(index, &item);
        if (FAILED(hr) || !item) {
            continue;
        }

        PWSTR path = nullptr;
        hr = item->GetDisplayName(SIGDN_FILESYSPATH, &path);
        item->Release();
        if (SUCCEEDED(hr) && path) {
            commandLine += L" ";
            commandLine += QuoteArg(path);
        }
        if (path) {
            CoTaskMemFree(path);
        }
    }

    std::vector<wchar_t> mutableCommand(commandLine.begin(), commandLine.end());
    mutableCommand.push_back(L'\0');

    STARTUPINFOW startupInfo = {};
    startupInfo.cb = sizeof(startupInfo);
    PROCESS_INFORMATION processInfo = {};
    BOOL ok = CreateProcessW(
        nullptr,
        mutableCommand.data(),
        nullptr,
        nullptr,
        FALSE,
        0,
        nullptr,
        nullptr,
        &startupInfo,
        &processInfo);
    if (!ok) {
        return HRESULT_FROM_WIN32(GetLastError());
    }

    CloseHandle(processInfo.hProcess);
    CloseHandle(processInfo.hThread);
    return S_OK;
}

class BatchPrintExplorerCommand final : public IExplorerCommand {
public:
    BatchPrintExplorerCommand() : refCount_(1) {
        InterlockedIncrement(&g_objectCount);
    }

    ~BatchPrintExplorerCommand() {
        InterlockedDecrement(&g_objectCount);
    }

    IFACEMETHODIMP QueryInterface(REFIID riid, void** ppv) override {
        if (!ppv) {
            return E_POINTER;
        }
        *ppv = nullptr;
        if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_IExplorerCommand)) {
            *ppv = static_cast<IExplorerCommand*>(this);
            AddRef();
            return S_OK;
        }
        return E_NOINTERFACE;
    }

    IFACEMETHODIMP_(ULONG) AddRef() override {
        return static_cast<ULONG>(InterlockedIncrement(&refCount_));
    }

    IFACEMETHODIMP_(ULONG) Release() override {
        ULONG count = static_cast<ULONG>(InterlockedDecrement(&refCount_));
        if (count == 0) {
            delete this;
        }
        return count;
    }

    IFACEMETHODIMP GetTitle(IShellItemArray*, PWSTR* name) override {
        return AllocShellString(L"\u7528\u6279\u91cf\u6253\u5370\u5de5\u5177\u6253\u5f00", name);
    }

    IFACEMETHODIMP GetIcon(IShellItemArray*, PWSTR* icon) override {
        return AllocShellString(ReadAppPath(), icon);
    }

    IFACEMETHODIMP GetToolTip(IShellItemArray*, PWSTR* tooltip) override {
        return AllocShellString(
            L"\u7528\u6279\u91cf\u6253\u5370\u5de5\u5177\u6253\u5f00\u9009\u4e2d\u7684\u6587\u4ef6\u548c\u6587\u4ef6\u5939",
            tooltip);
    }

    IFACEMETHODIMP GetCanonicalName(GUID* guidCommandName) override {
        if (!guidCommandName) {
            return E_POINTER;
        }
        *guidCommandName = CLSID_BatchPrintExplorerCommand;
        return S_OK;
    }

    IFACEMETHODIMP GetState(IShellItemArray*, BOOL, EXPCMDSTATE* state) override {
        if (!state) {
            return E_POINTER;
        }
        *state = ECS_ENABLED;
        return S_OK;
    }

    IFACEMETHODIMP Invoke(IShellItemArray* items, IBindCtx*) override {
        return LaunchBatchPrintKit(items);
    }

    IFACEMETHODIMP GetFlags(EXPCMDFLAGS* flags) override {
        if (!flags) {
            return E_POINTER;
        }
        *flags = ECF_DEFAULT;
        return S_OK;
    }

    IFACEMETHODIMP EnumSubCommands(IEnumExplorerCommand** enumCommands) override {
        if (!enumCommands) {
            return E_POINTER;
        }
        *enumCommands = nullptr;
        return E_NOTIMPL;
    }

private:
    long refCount_;
};

class ClassFactory final : public IClassFactory {
public:
    ClassFactory() : refCount_(1) {}

    IFACEMETHODIMP QueryInterface(REFIID riid, void** ppv) override {
        if (!ppv) {
            return E_POINTER;
        }
        *ppv = nullptr;
        if (IsEqualIID(riid, IID_IUnknown) || IsEqualIID(riid, IID_IClassFactory)) {
            *ppv = static_cast<IClassFactory*>(this);
            AddRef();
            return S_OK;
        }
        return E_NOINTERFACE;
    }

    IFACEMETHODIMP_(ULONG) AddRef() override {
        return static_cast<ULONG>(InterlockedIncrement(&refCount_));
    }

    IFACEMETHODIMP_(ULONG) Release() override {
        ULONG count = static_cast<ULONG>(InterlockedDecrement(&refCount_));
        if (count == 0) {
            delete this;
        }
        return count;
    }

    IFACEMETHODIMP CreateInstance(IUnknown* outer, REFIID riid, void** ppv) override {
        if (outer) {
            return CLASS_E_NOAGGREGATION;
        }
        BatchPrintExplorerCommand* command = new (std::nothrow) BatchPrintExplorerCommand();
        if (!command) {
            return E_OUTOFMEMORY;
        }
        HRESULT hr = command->QueryInterface(riid, ppv);
        command->Release();
        return hr;
    }

    IFACEMETHODIMP LockServer(BOOL lock) override {
        if (lock) {
            InterlockedIncrement(&g_lockCount);
        } else {
            InterlockedDecrement(&g_lockCount);
        }
        return S_OK;
    }

private:
    long refCount_;
};

STDAPI DllGetClassObject(REFCLSID rclsid, REFIID riid, void** ppv) {
    if (!IsEqualCLSID(rclsid, CLSID_BatchPrintExplorerCommand)) {
        return CLASS_E_CLASSNOTAVAILABLE;
    }
    ClassFactory* factory = new (std::nothrow) ClassFactory();
    if (!factory) {
        return E_OUTOFMEMORY;
    }
    HRESULT hr = factory->QueryInterface(riid, ppv);
    factory->Release();
    return hr;
}

STDAPI DllCanUnloadNow() {
    return (g_objectCount == 0 && g_lockCount == 0) ? S_OK : S_FALSE;
}

BOOL APIENTRY DllMain(HMODULE module, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        g_module = module;
        DisableThreadLibraryCalls(module);
    }
    return TRUE;
}
