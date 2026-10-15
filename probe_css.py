import re
s = open(r'D:\bianyiwenjianhuancun\xlsxviewer-ios\web\vendor\css\luckysheet.css', encoding='utf-8', errors='ignore').read()
ids = sorted(set(re.findall(r'#([a-zA-Z][\w-]*)', s)))
print(len(ids))
print(' '.join(ids))
# 找 sheets 相关容器定义
for kw in ['luckysheet-sheets', 'luckysheet-bottom', 'sheets']:
    idx = s.find(kw)
    if idx >= 0:
        print('---', kw, '---')
        print(s[max(0, idx-150):idx+200].replace('\n', ' ')[:350])
        print()
