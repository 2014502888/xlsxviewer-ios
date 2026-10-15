# 表格查看器（iOS 离线版）

功能等同 WPS 的**离线表格查看器**（不仿 WPS 品牌，名称/图标自定），支持编辑、筛选、选择/反选、求和、插入行列、升降序、合并、撤销重做、多表等。

- **技术**：WKWebView 壳 + Luckysheet（离线 UMD 全量打入 App）+ luckyexcel + SheetJS(xlsx)
- **完全离线**：所有 JS/CSS/字体打进 App，无网络请求
- **深浅色**：跟随系统自动切换，深色纯黑抬头/底部，表格黑底白字
- **打开**：App 内"打开"（UIDocumentPicker）+ 微信等"用其他应用打开"传入
- **保存**：保存为 xlsx 到沙盒（文件 App 可见"表格查看器"目录）
- **侧载**：unsigned IPA → TrollStore / 越狱自签

## 目录

```
ios/                 iOS 壳工程（XcodeGen）
  XlsxViewer/        Swift 壳（WKWebView + 原生桥）
  web/               离线前端资源（index.html / app.js / dark.css / vendor/）
.github/workflows/   GitHub Actions 云编译（macos-15 + xcodebuild，出 unsigned IPA）
web/                 本地 web 工程（src/ 为源）
```

## 编译

推送到 GitHub 仓库，Actions 自动编译产出 `XlsxViewer.ipa`（Payload 结构，未签名）。

## 原生桥协议（JS ↔ Swift）

| JS 动作 | 方向 | 说明 |
| --- | --- | --- |
| `callNative({action:'open'})` | JS→Swift | 弹出文件选择器 |
| `callNative({action:'readFile',name})` | JS→Swift | 读沙盒文件，Swift 回 `window.__onFileData(name, base64)` |
| `callNative({action:'save',name,data})` | JS→Swift | 保存 base64 到沙盒，回 `window.__onFileSaved(ok)` |
| `window.__onFileLoaded(name)` | Swift→JS | 外部打开/选择文件后通知页面 |
