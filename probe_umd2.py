import re
s = open(r'D:\bianyiwenjianhuancun\xlsxviewer-ios\web\vendor\luckysheet.umd.js', encoding='utf-8', errors='ignore').read()
# 找 toolbar 容器 HTML 模板
for m in re.finditer(r'class="([^"]*toolbar[^"]*)"[^>]*', s):
    pass
# 找包含 toolbar 的 div 模板片段
hits = [m.start() for m in re.finditer(r'<div[^>]*class="luckysheet-toolbar', s)]
print('div.luckysheet-toolbar:', len(hits))
for h in hits[:3]:
    print('   ', s[max(0,h-80):h+180].replace('\n', ' ')[:260])
    print()
# 顶部结构
for kw in ['luckysheet-info-window', 'luckysheet-formula-bar', 'luckysheet-toolbar-area', 'luckysheet-toolbar-wrap']:
    hits2 = [m.start() for m in re.finditer(re.escape(kw), s)]
    print(kw, len(hits2))
