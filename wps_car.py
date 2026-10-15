import subprocess, os
# 提取 WPS Assets.car 里的图片资源列表（有 assetutil 类工具更好，这里先看压缩资源结构）
car = r'D:\bianyiwenjianhuancun\xlsxviewer-ios\wps_ref\Payload\wpsoffice.app\Assets.car'
print('Assets.car size MB:', round(os.path.getsize(car)/1048576, 1))
data = open(car, 'rb').read()
# 找文件名（UTF-8 字符串 in car）
import re
names = set()
pat = re.compile(rb'[\x20-\x7e\xe4-\xe9][\x20-\x7e\x80-\xbf]{3,80}')
for m in pat.finditer(data[:min(len(data), 8000000)]):
    s = m.group().decode('utf-8', errors='ignore')
    if 'table' in s.lower() or 'toolbar' in s.lower() or 'cell' in s.lower() or 'sheet' in s.lower():
        names.add(s)
print('table/toolbar related:', len(names))
for n in sorted(names)[:30]:
    print('  ', n)
