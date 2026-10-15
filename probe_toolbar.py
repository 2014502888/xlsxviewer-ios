import re
s = open(r'D:\bianyiwenjianhuancun\xlsxviewer-ios\web\vendor\luckysheet.umd.js', encoding='utf-8', errors='ignore').read()
# 查 showtoolbarConfig / toolbarItems 相关配置
for kw in ['showtoolbarConfig', 'toolbarItems', 'showtoolbar', 'toolbarconfig']:
    hits = [m.start() for m in re.finditer(re.escape(kw), s, re.IGNORECASE)]
    print(kw, len(hits))
    for h in hits[:3]:
        print('   ', s[max(0,h-80):h+260].replace('\n', ' ')[:340])
        print()
