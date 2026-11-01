# Correções genéricas para PR no upstream

| Commit | O quê |
|---|---|
| f4b8b61 | `tests/jumptables_check.py`: oráculo segue o índice por `ubfx` (shift) e `table_load` segue o registrador do `br`. TotK 1.4.3 inalterado. |
| 0085dfa | `runtime/romfs.c` `romfs_list` + `fs_host.c`: `OpenDirectory` na RomFS (antes era fatal). |
