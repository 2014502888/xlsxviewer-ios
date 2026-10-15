import re
s = open(r'D:\bianyiwenjianhuancun\xlsxviewer-ios\web\vendor\luckysheet.umd.js', encoding='utf-8', errors='ignore').read()
for kw in ['luckysheet-sheets"', 'id="luckysheet-sheets', 'luckysheet-sheet-list', 'luckysheet-bottom-controll', 'luckysheet-info-window', 'luckysheet-toolbar"']:
    hits = [m.start() for m in re.finditer(re.escape(kw), s)]
    print(kw, len(hits))
    for h in hits[:2]:
        print('   ', s[max(0, h-130):h+160].replace('\n', ' ')[:290])
        print()
