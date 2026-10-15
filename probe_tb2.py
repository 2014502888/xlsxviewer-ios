import re
s = open(r'D:\bianyiwenjianhuancun\xlsxviewer-ios\web\vendor\luckysheet.umd.js', encoding='utf-8', errors='ignore').read()
# 提取 toobarConfig 对象全文
m = re.search(r'toobarConfig=\{([^}]*)\}', s)
if m:
    body = m.group(1)
    keys = re.findall(r'(\w+):\{ele:', body)
    print('toolbar buttons (%d):' % len(keys))
    print(' '.join(keys))
else:
    # 更大范围
    m2 = re.search(r'toobarConfig=\{(.{0,3000})\}', s, re.S)
    print('not found, trying 3000:', bool(m2))
    if m2:
        body = m2.group(1)
        keys = re.findall(r'(\w+):\{ele:', body)
        print('toolbar buttons (%d):' % len(keys))
        print(' '.join(keys))
