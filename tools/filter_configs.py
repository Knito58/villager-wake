"""Copy only the allowed config files from an instance into overrides/config and delete everything else there.

Usage: python3 tools/filter_configs.py <instance>/minecraft/config [overrides/config]
The allowlist is tools/config-allowlist.txt ("!" lines exclude). Run it after every instance update.
"""
import fnmatch, os, shutil, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, '..', 'overrides', 'config')
inc, exc = [], []
for line in open(os.path.join(here, 'config-allowlist.txt')):
    line = line.strip()
    if line and not line.startswith('#'):
        (exc if line.startswith('!') else inc).append(line.lstrip('!'))

def match(rel, pats):
    return any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(rel, p.replace('**', '*')) for p in pats)

keep = []
for root, _, files in os.walk(src):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), src).replace(os.sep, '/')
        if match(rel, inc) and not match(rel, exc):
            keep.append(rel)
if os.path.isdir(dst):
    shutil.rmtree(dst)
for rel in sorted(keep):
    os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
    shutil.copy2(os.path.join(src, rel), os.path.join(dst, rel))
print(f'{len(keep)} config files kept in {os.path.normpath(dst)}')
