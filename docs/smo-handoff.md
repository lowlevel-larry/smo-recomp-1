# SMO Recomp — handoff (onde parei / o que falta)

Leia isto primeiro ao retomar. Atualizado a cada passo. Plano completo: `docs/smo-plan.md`.

## Estado atual (2026-11-01)
- Fase: **F0 — repo e ambiente**
- Repo: `~/projects/smo-recomp`, git local, remote único `upstream` (valentderah/totk-pc-recomp, só fetch). Nunca push.
  - `main` = `upstream/main` (f469c5a, v0.2.8). Trabalho na branch `smo`.
- Dashboard: `python3 dashboard/server.py` → http://localhost:8787 (lê `progress.json`, fora do git).
  - Hooks do feed em `.claude/settings.local.json`: só valem numa sessão do `claude` aberta em `~/projects/smo-recomp`.
- Dumps: base `[0100000000010000][v0].nsp` (5.6 GB), update `[0100000000010800][v262144].nsp` (597 MB, = 1.4.x). NSP, sem NSZ.
  `prod.keys` e `title.keys` em `~/Downloads/Switch Dumps/`. Só leitura.
- Máquina: kernel 7.2.3 (ok ≥ 6.7), Vulkan 1.4 RADV com `VK_EXT_external_memory_host`.

## Feito
- [x] git init + upstream + branch smo + plano em docs/
- [x] dashboard rodando, progress.json criado

## Em andamento / próximo
- [ ] venvs (`.venv` 3.12, `.venv-py314`), `tools/fetch_refs.sh`, clonar OdysseyDecomp em `refs/`
- [ ] selftest sem jogo + `tests/diff/simd.py`, `atomic.py`, `flags_check.py`, `excl_mt.py`
- [ ] `tools/check_platform.py`
- [ ] `config.local.toml`
- [ ] F1: perfil SMO no extract.py, extrair 1.4.1, smo-target.md

## Bloqueios (dependem do usuário)
- Pacotes faltando: `sudo pacman -S --needed vulkan-headers vulkan-validation-layers` (sem `vulkan.h` o runtime não compila).
