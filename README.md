# Villager Wake

A Fabric modpack for Minecraft 26.1.2.

`prism-index/` holds the mod list as exported from the Prism Launcher instance
(one `.pw.toml` per mod).

## CurseForge check

The workflow **Check mods on CurseForge** (Actions tab, run manually) downloads
every jar of the pack and asks CurseForge which of them it knows, by file
fingerprint. Mods it does not know are looked up by name. The result lands in
`reports/curseforge-check.md`.
