#!/usr/bin/env python3
"""Copy JourneyMap waypoint GROUP presets (groups.preset.dat in this folder) into a world you pick.
Usage: python3 -I jm-copy-groups.py [world-name] [--dry]
Without a world name, it lists the worlds in ../saves and asks. Close Minecraft first.
A .bak of the target file is made. Waypoints are never touched. Mod-owned groups (e.g. Waystones) are skipped."""
import gzip,struct,sys,shutil,os,subprocess
here=os.path.dirname(os.path.abspath(__file__))
saves=os.path.join(here,'..','saves')
PRESET=os.path.join(here,'groups.preset.dat')
class R:
    def __init__(s,d): s.d=d;s.p=0
    def u(s,f):
        v=struct.unpack_from(f,s.d,s.p)[0];s.p+=struct.calcsize(f);return v
    def st(s):
        n=s.u('>H');v=s.d[s.p:s.p+n];s.p+=n;return v
    def pay(s,t):
        if t in(1,2,3,4,5,6):return (t,s.u({1:'>b',2:'>h',3:'>i',4:'>q',5:'>f',6:'>d'}[t]))
        if t==7:
            n=s.u('>i');v=s.d[s.p:s.p+n];s.p+=n;return (7,v)
        if t==8:return (8,s.st())
        if t==9:
            et=s.u('>b');n=s.u('>i');return (9,(et,[s.pay(et) for _ in range(n)]))
        if t==10:
            o={}
            while True:
                tt=s.u('>b')
                if tt==0:return (10,o)
                k=s.st();o[k]=s.pay(tt)
        if t==11:
            n=s.u('>i');v=s.d[s.p:s.p+4*n];s.p+=4*n;return (11,(n,v))
        if t==12:
            n=s.u('>i');v=s.d[s.p:s.p+8*n];s.p+=8*n;return (12,(n,v))
def load(path):
    r=R(gzip.open(path).read());t=r.u('>b');n=r.st();return n,r.pay(t)
def w(t,v,o):
    if t in(1,2,3,4,5,6):o.append(struct.pack({1:'>b',2:'>h',3:'>i',4:'>q',5:'>f',6:'>d'}[t],v))
    elif t==7:o.append(struct.pack('>i',len(v))+v)
    elif t==8:o.append(struct.pack('>H',len(v))+v)
    elif t==9:
        et,l=v;o.append(struct.pack('>bi',et,len(l)))
        for x in l:w(et,x[1],o)
    elif t==10:
        for k,(tt,vv) in v.items():
            o.append(struct.pack('>b',tt)+struct.pack('>H',len(k))+k);w(tt,vv,o)
        o.append(b'\0')
    elif t in(11,12):n,b=v;o.append(struct.pack('>i',n)+b)
def save(path,name,root):
    o=[struct.pack('>b',10)+struct.pack('>H',len(name))+name];w(10,root[1],o)
    with gzip.open(path,'wb') as f:f.write(b''.join(o))
def main():
    a=[x for x in sys.argv[1:] if not x.startswith('--')];dry='--dry' in sys.argv
    if subprocess.run(['pgrep','-f','[K]notClient'],capture_output=True).stdout.strip():sys.exit('Close Minecraft first.')
    f=lambda x:os.path.join(saves,x,'data','journeymap','player_waypoints.dat')
    if a: target=a[0]
    else:
        worlds=sorted((w for w in os.listdir(saves) if os.path.isfile(f(w))),key=lambda w:-os.path.getmtime(os.path.join(saves,w)))
        if not worlds:sys.exit('No worlds with JourneyMap data found in '+saves)
        print('Worlds (newest first):')
        for i,w in enumerate(worlds,1):print(f'  {i}) {w}')
        c=input('Target world number (empty = cancel): ').strip()
        if not c.isdigit() or not 1<=int(c)<=len(worlds):sys.exit('Cancelled.')
        target=worlds[int(c)-1]
    if not os.path.isfile(f(target)):sys.exit(f'{target}: no player_waypoints.dat yet. Open the world once in the game, quit, then retry.')
    _,src=load(PRESET);tn,dst=load(f(target))
    sp=next(iter(src[1][b'data'][1][b'groups_by_player'][1].values()))[1]
    dp=next(iter(dst[1][b'data'][1][b'groups_by_player'][1].values()))[1]
    for guid,(t,g) in sp.items():
        mod=g[b'modId'][1] if b'modId' in g else b''
        if mod!=b'journeymap' or guid==b'journeymap_all':continue
        nm=g[b'name'][1].decode()
        if guid in dp and guid!=b'journeymap_temp':print('keep existing',nm);continue
        print(('replace ' if guid in dp else 'add ')+nm);dp[guid]=(t,g)
    if dry:return
    shutil.copy2(f(target),f(target)+'.bak');save(f(target),tn,dst);print('written to',target,'(backup: player_waypoints.dat.bak)')
main()
