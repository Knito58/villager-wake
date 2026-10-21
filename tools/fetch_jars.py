"""Download every jar listed in prism-index/*.pw.toml into a target folder."""
import sys, tomllib, glob, os, urllib.request, hashlib

src, dest = sys.argv[1], sys.argv[2]
os.makedirs(dest, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, '*.pw.toml'))):
    d = tomllib.load(open(f, 'rb'))
    url, name = d['download']['url'], d['filename']
    out = os.path.join(dest, name)
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Knito58/villager-wake cf-check'})) as r:
        data = r.read()
    if hashlib.new(d['download']['hash-format'], data).hexdigest() != d['download']['hash']:
        sys.exit(f'hash mismatch: {name}')
    open(out, 'wb').write(data)
    print('ok', name)
