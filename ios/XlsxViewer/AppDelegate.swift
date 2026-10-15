import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        let window = UIWindow(frame: UIScreen.main.bounds)
        window.rootViewController = ViewController()
        window.makeKeyAndVisible()
        self.window = window
        return true
    }

    /// 微信等 App "用其他应用打开" 传入 xlsx 文件
    func application(_ app: UIApplication, open url: URL,
                     options: [UIApplication.OpenURLOptionsKey: Any] = [:]) -> Bool {
        guard url.isFileURL else { return false }
        // 拷贝到沙盒 files 目录并通知页面打开
        let destDir = ViewController.documentsDir().appendingPathComponent("files", isDirectory: true)
        try? FileManager.default.createDirectory(at: destDir, withIntermediateDirectories: true)
        let name = url.lastPathComponent
        let dest = destDir.appendingPathComponent(name)
        do {
            if FileManager.default.fileExists(atPath: dest.path) {
                try? FileManager.default.removeItem(at: dest)
            }
            try FileManager.default.copyItem(at: url, to: dest)
        } catch {
            return false
        }
        if let vc = window?.rootViewController as? ViewController {
            vc.openImportedFile(name: name)
        }
        return true
    }
}
