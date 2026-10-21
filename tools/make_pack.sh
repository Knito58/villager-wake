#!/usr/bin/env bash
# One-off: turn the Prism (Modrinth) mod list into a packwiz pack that uses CurseForge only.
# Result: pack/ (pack.toml, index.toml, mods/*.pw.toml, config files from overrides/),
# reports/make-pack.md and the CurseForge modpack zip in dist/
set -u
ROOT=$(pwd)
rm -rf pack && mkdir -p pack
python3 tools/fetch_jars.py prism-index pack/mods
cd pack
packwiz init --name "Villager Wake" --author Konitor --version 2.0.0 \
  --mc-version 26.1.2 --modloader fabric --fabric-version 0.19.5 -r
# many files are tagged 26.1 or 26.1.1 only; they run on 26.1.2 too
packwiz settings acceptable-versions 26.1,26.1.1
packwiz curseforge detect | tee "$ROOT/detect.log"
# jars CurseForge did not recognise by fingerprint are not kept
find mods -name '*.jar' -print -delete > "$ROOT/unmatched.txt"

REPORT="$ROOT/reports/make-pack.md"
{
  echo "# Villager Wake: building the CurseForge pack"
  echo
  echo "Matched by fingerprint: $(ls mods/*.pw.toml | wc -l). Not matched (left out unless added below): $(wc -l < "$ROOT/unmatched.txt")"
  echo
  echo "| Added by CurseForge slug/ID | Result |"
  echo "|---|---|"
} > "$REPORT"

add() {
  if out=$(packwiz -y curseforge add "$@" 2>&1); then r="ok: $(echo "$out" | grep -m1 '^Project .*successfully added' || echo added)"
  else r="FAILED: $(echo "$out" | tail -1)"; fi
  echo "| $* | ${r//|//} |" >> "$REPORT"
}
# mods on CurseForge, but not with the same file as in the Modrinth pack
for s in advancedfurnacey blooming-biosphere clientsort colossal-chests commandkeys cyclops-core \
         farming-for-blockheads modernfix-mvus player-armor-stands resourcestrees shogi \
         useful-structures villager-guards capabilityproxy everlastingabilities \
         bobby; do
  add "$s"
done
add --addon-id 1757335   # Create: Nerfad
# shader packs (pinned files; packwiz cannot pick shader files by loader)
add --addon-id 627557 --file-id 8884654   # Complementary Reimagined r5.9.3
add --addon-id 385587 --file-id 8884656   # Complementary Unbound r5.9.3
add --addon-id 1389097 --file-id 7824966   # Clarity 1.1.2 (replaces Nyxavora)

{
  echo
  echo "## Jars left out"
  echo
  sed 's/^mods\//- /' "$ROOT/unmatched.txt"
} >> "$REPORT"
# settings that belong to the pack (only what was changed on purpose)
cp -r "$ROOT/overrides/." .
packwiz refresh
mkdir -p "$ROOT/dist"
packwiz curseforge export -o "$ROOT/dist/villager-wake-2.0.0.zip"
