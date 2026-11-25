# Villager Wake

A Fabric modpack for Minecraft 26.3 (Fabric Loader 0.20.1, Java 25).

## Layout

- `prism-index/` holds the mod list as exported from the Prism Launcher instance
  (one `.pw.toml` per mod, each with its CurseForge project and file id).
- `instance/` is a snapshot of the Prism instance settings: `instance.cfg`
  (without local paths and play statistics), `mmc-pack.json`, `options.txt`
  and the shader pack list and options (`instance/shaderpacks/`). Jars,
  worlds, logs, caches and mod configs are not stored here.
- `overrides/jm-presets/` is shipped into the pack as `minecraft/jm-presets/`: JourneyMap
  group presets, the `jm-copy-groups.py` helper and the author's keybinds
  (`keybinds.options.txt`). See the README.txt in that folder.
- `overrides/config/` is the only place for mod configs. It holds only the
  settings that were changed on purpose (Starter Kit,
  Advanced Chimneys, Mineral Chance, Uncraft Everything,
  Waystones, Thief, Configurable Despawn Timer, Your Items Are Safe). They
  are copied into the pack.

## Shaders

Shaders run on the **Atmosphere Iris Fork** (CurseForge project 1798738,
`prism-index/atmosphere-iris-fork.pw.toml`), which replaces the official Iris
because Iris has no release for this Minecraft version yet. The fork is based on
Iris 1.11.6 and keeps the mod id `iris`, so other mods that depend on Iris still
resolve. It needs Sodium 0.9.x (included) and is not an official Iris build:
report problems to the Atmosphere author, not to the Iris team. The default
shader pack is Complementary Unbound; its settings are in `instance/shaderpacks/`.

## Billboard API (manual download)

Billboard API is not approved on CurseForge, so it is not in `prism-index/`
and not in the CurseForge pack. Billboard Engine is included and lists it only
as an optional dependency. Anyone who wants Billboard API has to download it
manually from its GitHub page and put the jar into the `mods` folder.

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
