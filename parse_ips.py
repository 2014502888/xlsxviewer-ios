import json
p = r'C:\Users\Administrator.DESKTOP-DC1E8KC\Desktop\XlsxViewer-2026-10-15-201031.ips'
lines = open(p, encoding='utf-8', errors='ignore').read().splitlines()
# .ips: 第 1 行是 JSON，后续是二进制/image 段
d = json.loads(lines[0])
print('app:', d.get('app_name'), '| ver:', d.get('app_version'), '| bundle:', d.get('bundleID'))
print('exception:', d.get('exception'))
print('termination:', d.get('termination'))
print('faultingThread:', d.get('faultingThread'))
print('asi:', d.get('asi'))
imgs = d.get('usedImages', [])
def imgname(idx):
    if idx is None or idx >= len(imgs): return '?'
    return imgs[idx].get('name', '?')
for t in d.get('threads', []):
    trig = t.get('triggered')
    tid = t.get('id')
    if trig or (d.get('faultingThread') is not None and tid == d.get('faultingThread')):
        print('== crashed thread', tid, t.get('name', ''), '==')
        for f in t.get('frames', [])[:22]:
            sym = f.get('symbol', '')
            print('   ', imgname(f.get('imageIndex')), '+', hex(f.get('imageOffset', 0)), sym)
