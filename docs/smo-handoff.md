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

- [x] F4 shaders: controle NVN do SDK 7 = **0x7d1 bytes** (c1/length +0x700/+0x704, stage +0x714, como no NVN 55).
  Runtime zera o resto até 0x880 (`gfx_shader.c control_view`); census `tools/smo_shader_census.py --translate`:
  10.965 shaders, 0 falhas. Todas as probes passam (vkexec desenha com shaders do SMO).
- [x] Rodando além do boot (`--seconds 10`): NVN 53.311 reportado ao SMO; `nvnQueueAcquireTexture` e
  `nvnDeviceApplyDeferredFinalizes` (`smo_nvn.c`); overrides SDK 7 em `smo_ov_system.c` (conta, settings, fs),
  `smo_ov_input.c` (hid direto ao serviço), `smo_ov_network.c` (offline: friends, nifm, bcat, pctl VR, prepo, socket, ssl).
  Saves em `build/profile-smo-v141/save/`.

## Onde parou
`TOTK_SHARED_FONTS=$PWD/build/substitute-fonts build/smo-v141/totk --seconds 10 --shot build/smo-v141/shot.png`
→ carrega as fontes compartilhadas e cai em `main+0x8dea04` (lookup de glifo devolve NULL na lib de fonte). Provável
glifo que só existe na fonte real (ícones de botão da "nintendo-extension"). As fontes substitutas (Noto,
`tools/smo_substitute_fonts.py`) são só para desenvolvimento.

## Próximo
1. Com o firmware do usuário: `.venv-py314/bin/python tools/extract_fonts.py --firmware <dir NCAs>` (ou
   `input.firmware` no config) → `build/extracted/firmware/shared-fonts`; rodar sem `TOTK_SHARED_FONTS`.
2. Seguir até o 1º frame (`--seconds 10 --shot`), item F4 frame; depois tela de título.
3. Pendências: `frame_rate.c player_pos`/`resolution.c`/`swkbd.c` ainda com constantes do TotK sob `!RT_SMO`;
   renomear binário para `smo`; alias `SMO_*` → `TOTK_*` em `cfg.c`; sync semanal com upstream.

## Bloqueios
- **Firmware do Switch** (para as fontes compartilhadas `nn::pl`): ver `docs/smo-blockers.md`.
