#!/usr/bin/env bash
# Build a packwiz pack and a CurseForge modpack zip from the Prism instance export.
# Input:  prism-index/*.pw.toml (mods), instance/shaderpacks/*.pw.toml (shaders), overrides/ (settings kept on purpose)
# Output: pack/, reports/make-pack.md, dist/villager-wake-<version>.zip
# Every entry in the Prism export carries its CurseForge project and file id, so no jars are downloaded.
set -u
ROOT=$(pwd)
VERSION=1.0.1
MC=26.3
FABRIC=0.20.1
rm -rf pack && mkdir -p pack reports dist
python3 tools/index_ids.py prism-index instance/shaderpacks > "$ROOT/ids.txt" || { echo "entries without CurseForge id, see above"; exit 1; }
cd pack
packwiz init --name "Villager Wake" --author Konitor --version "$VERSION" \
  --mc-version "$MC" --modloader fabric --fabric-version "$FABRIC" -r

REPORT="$ROOT/reports/make-pack.md"
{
  echo "# Villager Wake: building the CurseForge pack"
  echo
  echo "| Mod | Project | File | Result |"
  echo "|---|---|---|---|"
} > "$REPORT"
while read -r pid fid name; do
  if out=$(packwiz -y curseforge add --addon-id "$pid" --file-id "$fid" 2>&1); then r=ok
  else r="FAILED: $(echo "$out" | tail -1)"; fi
  echo "| $name | $pid | $fid | ${r//|//} |" >> "$REPORT"
done < "$ROOT/ids.txt"

# packwiz also adds the required dependencies of every mod on its own. The pack must contain exactly
# the mods of the Prism instance, so everything else is removed again and listed in the report.
# (1.0.0 shipped "Create Fly: Unofficial port" this way: a second jar with mod id "create", which
# Fabric preferred over Create Fly and which broke joining the server.)
awk '{print $1}' "$ROOT/ids.txt" | sort -u > "$ROOT/ids-wanted.txt"
for f in mods/*.pw.toml; do
  [ -e "$f" ] || continue
  pid=$(sed -n 's/^project-id = //p' "$f" | head -1)
  if ! grep -qx "$pid" "$ROOT/ids-wanted.txt"; then
    dep=$(sed -n 's/^name = "\(.*\)"/\1/p' "$f" | head -1)
    echo "| ${dep// /_} | $pid | | REMOVED: added as dependency, not in the Prism instance |" >> "$REPORT"
    rm -f "$f"
  fi
done
rm -f "$ROOT/ids.txt" "$ROOT/ids-wanted.txt"

# settings that belong to the pack (only what was changed on purpose)
cp -r "$ROOT/overrides/." .
packwiz refresh
packwiz curseforge export -o "$ROOT/dist/villager-wake-$VERSION.zip"
