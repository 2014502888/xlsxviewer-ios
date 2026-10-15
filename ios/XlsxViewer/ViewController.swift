import UIKit
import WebKit

class ViewController: UIViewController, WKScriptMessageHandler, UIDocumentPickerDelegate, WKNavigationDelegate {

    var webView: WKWebView!
    private var pendingFileName: String?

    static func documentsDir() -> URL {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground

        let config = WKWebViewConfiguration()
        let bridge = WKUserContentController()
        bridge.add(self, name: "xlsxBridge")
        config.userContentController = bridge
        // 注意：不加任何私有 KVC（setValue:forKey: "allowUniversalAccessFromFileURLs" 等）
        // iOS 16.5 上会抛 NSUnknownKeyException 直接崩溃；loadFileURL(allowingReadAccessTo:) 已足够

        webView = WKWebView(frame: view.bounds, configuration: config)
        webView.navigationDelegate = self
        webView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        webView.isOpaque = false
        view.addSubview(webView)

        loadWebApp()
    }

    private func loadWebApp() {
        // bundle 内 web 文件夹（XcodeGen folder resource 保留目录结构）
        guard let base = Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "web"),
              let webDir = Bundle.main.resourceURL?.appendingPathComponent("web") else { return }
        webView.loadFileURL(base, allowingReadAccessTo: webDir)
    }

    func openImportedFile(name: String) {
        guard let wv = webView else { pendingFileName = name; return }
        // 页面未加载完成时先挂起，didFinish 后再打开
        if wv.isLoading || wv.url == nil {
            pendingFileName = name
            return
        }
        let js = "window.__onFileLoaded('\(escaped(name))')"
        wv.evaluateJavaScript(js) { _, _ in }
    }

    private func escaped(_ s: String) -> String {
        s.replacingOccurrences(of: "\\", with: "\\\\")
         .replacingOccurrences(of: "'", with: "\\'")
         .replacingOccurrences(of: "\n", with: "\\n")
    }

    // MARK: - WKScriptMessageHandler
    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        guard message.name == "xlsxBridge",
              let body = message.body as? [String: Any] else { return }
        let action = body["action"] as? String ?? ""

        switch action {
        case "open":
            presentDocumentPicker()
        case "readFile":
            guard let name = body["name"] as? String else { return }
            sendFileData(name: name)
        case "save":
            guard let name = body["name"] as? String, let base64 = body["data"] as? String else { return }
            saveBase64(name: name, base64: base64)
        default:
            break
        }
    }

    // MARK: - 打开文件（UIDocumentPicker）
    private func presentDocumentPicker() {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [
            .spreadsheet,
            .commaSeparatedText,
            .data
        ], asCopy: true)
        picker.delegate = self
        present(picker, animated: true)
    }

    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
        guard let url = urls.first else { return }
        let name = url.lastPathComponent
        let destDir = ViewController.documentsDir().appendingPathComponent("files", isDirectory: true)
        try? FileManager.default.createDirectory(at: destDir, withIntermediateDirectories: true)
        let dest = destDir.appendingPathComponent(name)
        do {
            if FileManager.default.fileExists(atPath: dest.path) {
                try? FileManager.default.removeItem(at: dest)
            }
            try FileManager.default.copyItem(at: url, to: dest)
        } catch {
            return
        }
        openImportedFile(name: name)
    }

    func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
    }

    // MARK: - 读取沙盒文件 → base64 回传 JS
    private func sendFileData(name: String) {
        let fileURL = ViewController.documentsDir().appendingPathComponent("files").appendingPathComponent(name)
        guard let data = try? Data(contentsOf: fileURL) else {
            let js = "alert('文件不存在：\(escaped(name))')"
            webView.evaluateJavaScript(js, completionHandler: nil)
            return
        }
        let base64 = data.base64EncodedString()
        let js = "window.__onFileData('\(escaped(name))', '\(base64)')"
        webView.evaluateJavaScript(js, completionHandler: nil)
    }

    // MARK: - 保存 base64 → 沙盒 files 目录
    private func saveBase64(name: String, base64: String) {
        let destDir = ViewController.documentsDir().appendingPathComponent("files", isDirectory: true)
        try? FileManager.default.createDirectory(at: destDir, withIntermediateDirectories: true)
        let dest = destDir.appendingPathComponent(name)
        guard let data = Data(base64Encoded: base64) else { return }
        do {
            try data.write(to: dest)
            // 提示用户可通过"文件"App 访问
            let js = "window.__onFileSaved(true)"
            webView.evaluateJavaScript(js, completionHandler: nil)
        } catch {
            let js = "window.__onFileSaved(false)"
            webView.evaluateJavaScript(js, completionHandler: nil)
        }
    }

    // MARK: - WKNavigationDelegate
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        // 页面就绪后，若启动时有待打开文件（openImportedFile 早于页面加载完成）
        if let name = pendingFileName {
            pendingFileName = nil
            openImportedFile(name: name)
        }
    }

    override var prefersStatusBarHidden: Bool { false }

    // 状态栏跟随深浅色：深色白字、浅色黑字（铁律）
    override var preferredStatusBarStyle: UIStatusBarStyle {
        if traitCollection.userInterfaceStyle == .dark { return .lightContent }
        return .darkContent
    }
    override func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
        super.traitCollectionDidChange(previousTraitCollection)
        if previousTraitCollection?.userInterfaceStyle != traitCollection.userInterfaceStyle {
            setNeedsStatusBarAppearanceUpdate()
        }
    }
}
