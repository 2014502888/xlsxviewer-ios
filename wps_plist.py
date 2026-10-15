import plistlib, os, re
app = r'D:\bianyiwenjianhuancun\xlsxviewer-ios\wps_ref\Payload\wpsoffice.app'
with open(os.path.join(app, 'Info.plist'), 'rb') as f:
    p = plistlib.load(f)
def show(k):
    v = p.get(k)
    if v is not None:
        print(k, '=', v if not isinstance(v, (list, dict)) else str(v)[:200])
for k in ['CFBundleDisplayName', 'CFBundleName', 'CFBundleIdentifier', 'CFBundleShortVersionString',
          'MinimumOSVersion', 'UIRequiredDeviceCapabilities', 'CFBundleDocumentTypes', 'LSApplicationQueriesSchemes',
          'UISupportedInterfaceOrientations', 'UIStatusBarStyle', 'UIUserInterfaceStyle']:
    show(k)
# 文档类型（表格相关）
dt = p.get('CFBundleDocumentTypes') or []
for d in dt[:6]:
    print('--- doc type:', d.get('CFBundleTypeName'))
    print('   contentTypes:', d.get('LSItemContentTypes'))
