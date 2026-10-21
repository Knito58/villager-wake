"""Look up CurseForge projects by URL path through api.cfwidget.com and list their newest files."""
import sys, json, urllib.request, datetime

paths = [p.strip() for p in sys.argv[1].split(';') if p.strip()]
L = ['# CurseForge lookup (cfwidget)', '', f'Run {datetime.date.today()}.', '']
for path in paths:
    try:
        req = urllib.request.Request(f'https://api.cfwidget.com/{path}', headers={'User-Agent': 'Knito58/villager-wake'})
        with urllib.request.urlopen(req, timeout=60) as r:
            j = json.load(r)
    except Exception as e:
        L += [f'## {path}', '', f'not found ({e})', '']
        continue
    L += [f"## {j.get('title')} ({path})", '', f"ID {j.get('id')}, {j.get('urls', {}).get('curseforge', '')}", '',
          '| File | Versions | Date |', '|---|---|---|']
    for f in sorted(j.get('files', []), key=lambda f: f.get('uploaded_at', ''), reverse=True)[:6]:
        L.append(f"| {f.get('name')} | {', '.join(f.get('versions', []))} | {f.get('uploaded_at', '')[:10]} |")
    L.append('')
open(sys.argv[2], 'w').write('\n'.join(L) + '\n')
