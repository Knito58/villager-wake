# Villager Wake

A Fabric modpack for Minecraft 26.3 (Fabric Loader 0.20.1, Java 25).

## Layout

- `prism-index/` holds the mod list as exported from the Prism Launcher instance
  (one `.pw.toml` per mod, each with its CurseForge project and file id).
- `instance/` is a snapshot of the Prism instance settings: `instance.cfg`
  (without local paths and play statistics), `mmc-pack.json`, `options.txt`
  and the shader pack list and options (`instance/shaderpacks/`). Jars,
  worlds, logs, caches and mod configs are not stored here.
- `overrides/config/` is the only place for mod configs. It holds only the
  settings that were changed on purpose (Starter Kit,
  Tiered Backpacks, Advanced Chimneys, Mineral Chance, Uncraft Everything,
  Waystones, Thief, Configurable Despawn Timer, Your Items Are Safe). They
  are copied into the pack.

## Building the pack

The workflow **Make CurseForge pack** (Actions tab, run manually) builds `pack/`
(a packwiz pack) from the CurseForge ids in `prism-index/` and
`instance/shaderpacks/`, adds `overrides/`, and writes the CurseForge modpack
zip to `dist/` and a result table to `reports/make-pack.md`.

## Updating the configs

After every instance update run
`python3 tools/filter_configs.py "<instance>/minecraft/config"`.
It rebuilds `overrides/config/` from the allowlist in
`tools/config-allowlist.txt` and removes every other config file. Add a mod
to the allowlist only when its settings were changed on purpose.
