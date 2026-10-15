import re, os
# 从 WPS 主二进制提取中文界面文案（表格相关），避免全量 dump
bin_path = r'D:\bianyiwenjianhuancun\xlsxviewer-ios\wps_ref\Payload\wpsoffice.app\wpsoffice'
# 用纯 python 扫 UTF-8 中文串（二进制里字符串是 UTF-8/UTF-16 混合；先扫 UTF-8）
data = open(bin_path, 'rb').read()
print('binary size MB:', round(len(data)/1048576, 1))
# UTF-8 中文串（长度 4~40）
pat = re.compile(rb'[\xe4-\xe9][\x80-\xbf][\x80-\xbf](?:[\xe0-\xe9][\x80-\xbf][\x80-\xbf]|[\x00-\x7f]){3,80}')
hits = set()
for m in pat.finditer(data):
    s = m.group().decode('utf-8', errors='ignore')
    if len(s) >= 4 and any('\u4e00' <= c <= '\u9fff' for c in s):
        hits.add(s)
print('unique zh strings:', len(hits))
kws = ['筛选', '排序', '求和', '冻结', '合并', '插入', '删除', '单元格', '格式', '填充', '边框', '查找', '替换', '撤销', '重做', '复制', '粘贴', '字体', '对齐']
for kw in kws:
    m = [s for s in hits if kw in s]
    if m:
        print(f'== {kw} ({len(m)}) ==')
        for s in sorted(m)[:8]:
            print('   ', s)
