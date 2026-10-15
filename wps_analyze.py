import zipfile
p = r'C:\Users\Administrator.DESKTOP-DC1E8KC\Desktop\wpsoffice-11.15.1.ipa'
z = zipfile.ZipFile(p)
names = z.namelist()
print('total files:', len(names))
apps = sorted(set(n.split('/')[1] for n in names if n.startswith('Payload/') and n.count('/') >= 2))
print('app bundle:', apps)
tops = {}
for n in names:
    parts = n.split('/')
    if len(parts) > 3:
        key = parts[3]
        tops[key] = tops.get(key, 0) + 1
for k, v in sorted(tops.items(), key=lambda x: -x[1])[:25]:
    print(f'{k:40s} {v}')
