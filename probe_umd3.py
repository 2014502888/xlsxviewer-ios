import re
s = open(r'D:\bianyiwenjianhuancun\xlsxviewer-ios\web\vendor\luckysheet.umd.js', encoding='utf-8', errors='ignore').read()
for kw in ['id="luckysheet-toolbar', 'id="luckysheet-sheets"', 'id="luckysheet-count-bar', 'id="luckysheet-info-window', 'luckysheet-bottom-controll-row"', 'id="luckysheet-functionbox"', 'id="luckysheet-formula']:
    hits = [m.start() for m in re.finditer(re.escape(kw), s)]
    print(kw, len(hits))
    for h in hits[:2]:
        ctx = s[max(0, h-60):h+150].replace('\n', ' ')
        print('   ', ctx[:210])
        print()
