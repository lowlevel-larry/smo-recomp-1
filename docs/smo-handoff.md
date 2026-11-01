# SMO Recomp — handoff (onde parei / o que falta)

Leia isto primeiro ao retomar. Atualizado a cada passo. Plano completo: `docs/smo-plan.md`. Alvo: `docs/smo-target.md`.

## Estado atual (2026-11-01)
- Fase: **F2 — lift e link** (lift ok, cobertura 100%, jump tables 0 divergências; compilando)
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

- [x] F2 lift: `.venv/bin/python recomp/gen.py --exefs build/extracted/smo-v141/exefs --out generated/smo-v141`
  (genérico, sem mudança; 102.327 funções, 0 unsupported, ~20 s, 336 MB de C)
- [x] F2 `tools/smo_scan_sites.py`: cobertura 100% (60 SVC, 99 MRS, 12 MSR, 4.763 exclusivas, x18, 1.175 jump tables)
- [x] F2 `tests/jumptables_check.py --exefs build/extracted/smo-v141/exefs`: 0 divergências, exit 0
  (corrigi o oráculo do teste: índice via ubfx e table_load; commit separado, upstreamable)

## Próximo
1. Build: `.venv/bin/python tools/build_game.py --version smo-v141 --expected tools/data/smo-expected-v1.4.1.json`
   (log em `build/logs/build-smo-v141.log`; binário sai como `build/smo-v141/totk` — renomear para `smo` depois).
2. `build/smo-v141/totk --selftest` → fecha F2 link e F0 ambiente.
3. F3: inventário `nn::*` (`docs/smo-sdk-gap.md`): imports do main vs `HOST_OVERRIDE` existentes.

## Bloqueios
- Nenhum.
