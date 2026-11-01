# SMO Recomp — handoff (onde parei / o que falta)

Leia isto primeiro ao retomar. Atualizado a cada passo. Plano completo: `docs/smo-plan.md`. Alvo: `docs/smo-target.md`.

## Estado atual (2026-11-01)
- Fase: **F1 quase completa → F2 (lift e link)**
- Repo: `~/projects/smo-recomp`, branch `smo`, remote único `upstream`. Nunca push. `main` = upstream f469c5a.
- Dashboard: `python3 dashboard/server.py` → **http://127.0.0.1:8787** (`localhost` pode ir para IPv6 e falhar).
- Versão suportada: **só 1.4.1** (pedido do usuário). Update: `...[0100000000010800][v393216][Update v1.4.1].nsp`.
  O dump antigo (v262144) era 1.3.0 e foi substituído pelo usuário.
- Extração: `.venv-py314/bin/python tools/smo_extract.py` (versão lida do NACP; reexecução verifica hashes).
  Saída: `build/extracted/smo-v0/exefs` (1.0.0, para mapear o decomp) e `build/extracted/smo-v141/{exefs,romfs}`.
- Ambiente: venvs `.venv` (3.12) e `.venv-py314`, `refs/` + `refs/OdysseyDecomp`, hactool em `toolchain/hactool`.
  Máquina atual: GPU AMD Renoir (RADV); a RTX 5050 não aparece aqui.

## Feito
- [x] F0 repo/branch/plano; dashboard; `config.local.toml`
- [x] F0 testes do lifter: simd (159.976 casos), atomic (12.672), flags_check, check_platform → 0 falhas
  - `excl_mt.py` ABA falha **por design upstream** (monitor exclusivo = CAS, não detecta X→Y→X). Não é Linux.
- [x] F1 `tools/smo_profile.py`, `tools/smo_extract.py`, `tools/smo_target_info.py`, `smo-expected-v1.4.1.json`
- [x] F1 `docs/smo-target.md` (falta só a revisão do audren, que sai no 1º boot)

## Próximo
1. F2: ver como `recomp/gen.py` / `layout.py` escolhem módulos e versão (são amarrados a v121/v143) e adicionar o
   perfil SMO com o mínimo de diff. Rodar `gen.py` em main/sdk/subsdk0 da 1.4.1.
2. `tools/smo_scan_sites.py` (oráculo de cobertura), `tests/jumptables_check.py` no SMO.
3. `tools/build_game.py` → binário `smo` + `--selftest` (fecha também o item F0 ambiente).

## Bloqueios
- Nenhum.
