# SMO Recomp — handoff (onde parei / o que falta)

Leia isto primeiro ao retomar. Atualizado a cada passo. Plano completo: `docs/smo-plan.md`. Alvo: `docs/smo-target.md`.

## Estado atual
- Fase: **F4 — gráficos** (F0–F3 concluídas). Próximo foco: layout da seção de controle NVN do SDK 7.
- Repo: `~/projects/smo-recomp`, branch `smo`, remote único `upstream`. Nunca push. `main` = upstream f469c5a.
- Dashboard: `python3 dashboard/server.py` → **http://127.0.0.1:8787**.
- Versão suportada: **só 1.4.1**. Binário: `build/smo-v141/totk` (renomear para `smo` depois).
- Build: `.venv/bin/python recomp/gen.py --exefs build/extracted/smo-v141/exefs --out generated/smo-v141` e
  `.venv/bin/python tools/build_game.py --version smo-v141 --expected tools/data/smo-expected-v1.4.1.json` (~3 min).
- `RT_SMO` (host.h) = build `smo-v*`; `rt_game_version` = 141 (RT_V143/RT_V111 falsos → SMO cai no caminho 1.2.1
  onde não houver `RT_SMO`). Pontos TotK-específicos ainda sem guarda: `frame_rate.c player_pos` (lê main+offset do
  TotK, protegido por read_guest), `resolution.c`, `swkbd.c ARG_WORK`, `ipc.c` probe de áudio.

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

- [x] F2 link + `--selftest` (0 falhas) — também fecha F0 ambiente
- [x] F3 `docs/smo-sdk-gap.md` (`tools/smo_sdk_gap.py`): 566 nn::, 62 com override idêntico, 0 assinatura diferente
- [x] F3 `--boot` passa: SDK init, DT_INIT (191/44/106), nnMain, RomFS montada, 1ª NVN
  `nvnBootstrapLoader("nvnDeviceInitialize")` de main+0x9413f4. SDK 7: `nn::init::Start(h, args, loader_ready,
  module_inits)` (4 args). SMO chama NVN antes de SetFocusHandlingMode (tail call em main+0x5743b8).
- [x] F4 probes: gfx-abi, nvn, nvn-tex, vkmem, kernel, loader (com `expect_smo`) passam.
- [~] F4 shaders: tradutor compilado (`tools/build_xlate.py`), `tools/smo_shader_census.py` escrito, mas acha **0 shaders**:
  os `.sharcb` (agl, dentro de `ShaderData/*.szs` Yaz0+SARC) têm a seção de controle NVN **do SDK 7**: magic
  0x98761234 presente, mas registros com tamanho 0x861/0x86d (TotK: 0x880/0x88c) e em +0x700 não há (c1, length).
  Ex.: `alCloudShader.sharcb`, 24 controles, 1º em +0x11c8; palavras +0x8: 1, 9, 0x120, 0xb, 0x7d0, 0, 0, 0x7d1.

## Próximo
1. Descobrir o layout do controle NVN do SDK 7 (onde ficam stage, offset/tamanho do código, local size de compute).
   Fontes: Ryujinx (MIT) `ShaderProgramInfo`/NVN parsing, d2r-mobile, deko3d (`refs/deko3d`), Switchbrew. Depois:
   - `smo_shader_census.py` com parser SDK 7; `--probe-vkexec` acha jobs em `build/v141/shaders` (o probe usa
     `build/v%d`: alinhar com `build/smo-v141`).
   - Conferir o caminho de programa do runtime (`nvn_api_*`: chave do shader lê control[:0x880]).
2. Rodar além do boot: `build/smo-v141/totk --seconds 10 --shot out.png` → primeiro frame (item F4 frame).
3. Antigo passo 1. Build: `.venv/bin/python tools/build_game.py --version smo-v141 --expected tools/data/smo-expected-v1.4.1.json`
   (log em `build/logs/build-smo-v141.log`; binário sai como `build/smo-v141/totk` — renomear para `smo` depois).
2. `build/smo-v141/totk --selftest` → fecha F2 link e F0 ambiente.
3. F3: inventário `nn::*` (`docs/smo-sdk-gap.md`): imports do main vs `HOST_OVERRIDE` existentes.

## Bloqueios
- Nenhum.
