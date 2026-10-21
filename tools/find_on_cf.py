"""Search CurseForge (through packwiz) for each name and note what packwiz would add for MC 26.1.2 Fabric."""
import sys, os, subprocess, tomllib, glob, shutil, datetime

names = [n.strip() for n in sys.argv[1].split(';') if n.strip()]
out = sys.argv[2]
rows = []
for name in names:
    work = os.path.join('work-find', name.replace('/', '_'))
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    subprocess.run(['packwiz', 'init', '--name', 'find', '--author', 'find', '--version', '0',
                    '--mc-version', '26.1.2', '--modloader', 'fabric', '--fabric-version', '0.19.3', '-r'],
                   cwd=work, check=True, capture_output=True)
    # shader and resource packs are often tagged with older versions only
    subprocess.run(['packwiz', 'settings', 'acceptable-versions',
                    '26.1,26.1.1,26.2,26.3,1.21.11,1.21.10,1.21.9,1.21.8,1.21.7,1.21.6,1.21.5,1.21.4,1.21'],
                   cwd=work, capture_output=True, text=True)
    p = subprocess.run(['packwiz', '-y', 'settings', 'acceptable-versions', '26.1,26.1.1,1.21.11'],
                       cwd=work, capture_output=True, text=True)
    print('settings:', p.returncode, p.stdout, p.stderr)
    p = subprocess.run(['packwiz', '-y', 'curseforge', 'add', name], cwd=work, capture_output=True, text=True)
    log = (p.stdout + p.stderr).strip().splitlines()
    found = []
    for f in sorted(glob.glob(os.path.join(work, '**', '*.pw.toml'), recursive=True)):
        d = tomllib.load(open(f, 'rb'))
        found.append(f"{d['name']} (`{os.path.basename(f)[:-8]}`, `{d['filename']}`)")
    if found:
        rows.append((name, 'found', '<br>'.join(found)))
    else:
        rows.append((name, 'not added', (log[-1] if log else '').replace('|', '/')))
    print(name, '->', rows[-1][1])

L = ['# Villager Wake: CurseForge search', '',
     f'Run {datetime.date.today()}. Search term, then what packwiz would add for Minecraft 26.1.2 / Fabric',
     '(first search hit; the hit may be a different mod with a similar name, so check the slug).', '',
     '| Search term | Result | Added (name, CurseForge slug, file) or last message |', '|---|---|---|']
L += [f'| {a} | {b} | {c} |' for a, b, c in rows]
open(out, 'w').write('\n'.join(L) + '\n')
