"""Compare the Prism mod list with what packwiz found on CurseForge; write a Markdown report."""
import sys, tomllib, glob, os, json, urllib.request, datetime

index_dir, work_mods, out = sys.argv[1], sys.argv[2], sys.argv[3]

found = {}  # jar filename -> curseforge metadata
for f in glob.glob(os.path.join(work_mods, '*.pw.toml')):
    d = tomllib.load(open(f, 'rb'))
    cf = d['update']['curseforge']
    found[d['filename']] = (os.path.basename(f)[:-len('.pw.toml')], cf['project-id'])

def cfwidget(slug):
    try:
        req = urllib.request.Request(f'https://api.cfwidget.com/minecraft/mc-mods/{slug}',
                                     headers={'User-Agent': 'Knito58/villager-wake cf-check'})
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.load(r)
        return j.get('id'), j.get('urls', {}).get('curseforge', '')
    except Exception:
        return None, ''

same, other, missing = [], [], []
for f in sorted(glob.glob(os.path.join(index_dir, '*.pw.toml'))):
    d = tomllib.load(open(f, 'rb'))
    slug = os.path.basename(f)[:-len('.pw.toml')]
    if d['filename'] in found:
        cfslug, pid = found[d['filename']]
        same.append((d['name'], d['filename'], cfslug, pid))
        continue
    pid, url = cfwidget(slug)
    (other if pid else missing).append((d['name'], d['filename'], slug, pid, url))

key = lambda r: r[0].lower()
L = [f'# Villager Wake: CurseForge check',
     '',
     f'Run {datetime.date.today()} on {len(same) + len(other) + len(missing)} mods.',
     '',
     f'- **Same file on CurseForge:** {len(same)}',
     f'- **Mod found on CurseForge by name, but not this exact file:** {len(other)} (check version by hand)',
     f'- **Not found on CurseForge:** {len(missing)}',
     '',
     'Third-party distribution (needed for Prism) is not checked here.',
     '',
     '## Not found on CurseForge', '', '| Mod | File | Modrinth slug |', '|---|---|---|']
L += [f'| {n} | `{fn}` | {s} |' for n, fn, s, _, _ in sorted(missing, key=key)]
L += ['', '## Found by name, other file', '', '| Mod | File | CurseForge |', '|---|---|---|']
L += [f'| {n} | `{fn}` | [{pid}]({u}) |' for n, fn, s, pid, u in sorted(other, key=key)]
L += ['', '## Same file on CurseForge', '', '| Mod | File | CurseForge slug | Project ID |', '|---|---|---|---|']
L += [f'| {n} | `{fn}` | {s} | {pid} |' for n, fn, s, pid in sorted(same, key=key)]
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w').write('\n'.join(L) + '\n')
print(f'same={len(same)} other={len(other)} missing={len(missing)}')
