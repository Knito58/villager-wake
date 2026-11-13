"""Print "<project-id> <file-id> <name>" for every CurseForge entry of the given .pw.toml folders.
Entries without CurseForge ids are listed on stderr and make the script exit 1."""
import glob, sys, tomllib

missing = 0
for folder in sys.argv[1:]:
    for f in sorted(glob.glob(f'{folder}/*.pw.toml')):
        d = tomllib.load(open(f, 'rb'))
        cf = d.get('update', {}).get('curseforge')
        if not cf:
            print(f'no CurseForge id: {f}', file=sys.stderr)
            missing += 1
            continue
        print(cf['project-id'], cf['file-id'], d['name'].replace(' ', '_'))
sys.exit(1 if missing else 0)
