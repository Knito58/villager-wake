#!/usr/bin/env bash
# Build a packwiz pack and a CurseForge modpack zip from the Prism instance export.
# Input:  prism-index/*.pw.toml (mods), instance/shaderpacks/*.pw.toml (shaders), overrides/ (settings kept on purpose)
# Output: pack/, reports/make-pack.md, dist/villager-wake-<version>.zip
# Every entry in the Prism export carries its CurseForge project and file id, so no jars are downloaded.
set -u
ROOT=$(pwd)
VERSION=3.0.0
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
rm -f "$ROOT/ids.txt"

# settings that belong to the pack (only what was changed on purpose)
cp -r "$ROOT/overrides/." .
packwiz refresh
packwiz curseforge export -o "$ROOT/dist/villager-wake-$VERSION.zip"
