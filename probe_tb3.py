import re
s = open(r'D:\bianyiwenjianhuancun\xlsxviewer-ios\web\vendor\luckysheet.umd.js', encoding='utf-8', errors='ignore').read()
i = s.find('toobarConfig=')
seg = s[i:i+20000]
# 括号配平提取对象
depth = 0; start = -1; end = -1
for j, ch in enumerate(seg):
    if ch == '{':
        if depth == 0: start = j
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0 and start >= 0:
            end = j; break
obj = seg[start:end+1]
keys = re.findall(r'(\w+):\{ele:', obj)
print('toolbar buttons (%d):' % len(keys))
print(' '.join(keys))
