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
  Saves: `~/.local/share/smo-recomp/profile/save/` pelo `tools/run_safe.sh` (TOTK_PROFILE_DIR; fora do build/).

- [x] Fontes sem firmware: o `nn::fontll` do SDK 7 quer o sfnt decodificado (runtime decodifica o BFTTF para o SMO);
  `tools/smo_substitute_fonts.py` gera 6 fontes livres distintas (Noto/Liberation) em `build/substitute-fonts`.
- [x] `GetPerformanceConfiguration`; `OpenDirectory` na RomFS (`romfs_list`, upstreamable).
- [x] `runtime/smo_*.c` só entra em build `smo-v*` (build_game.py); build TotK do runtime conferida sem eles.
- [x] **Roda a 60 fps estáveis** (3 min sem crash), áudio aberto, janela 1920x1080. O jogo renderiza o menu de
  primeira execução ("Start / Start in Assist Mode") corretamente no alvo interno 1600x900 rgb10a2.

## Onde parou
Rodar: `tools/run_safe.sh` (lavapipe, não trava a GPU) ou `tools/run_safe.sh --gpu`; binário é `build/smo-v141/smo`.
GPU travando derruba o Hyprland: rode o Claude com `claude-safe` (tmux fora do Hyprland).
**Travamento na GPU real (RADV Renoir, Mesa 26.2), 2026-11-01 — contornado:** `ring gfx timeout` com o gravador
assíncrono de comandos (`vk_rec.c`) ligado: com overlay `full` travava de 5 s a 1,5 min; com `TOTK_VK_RECORDER=0` 12 min
limpos a 60 fps (o gravador não ganha nada aqui). SMO agora tem o gravador desligado por padrão (`vk_rec.c rec_begin`).
A causa dentro do gravador não foi achada: todo `vkCmd*` passa pelos wrappers `rc_*`/`rec_*`, então não é gravação direta;
o suspeito é tempo de vida de objeto reciclado antes de o gravador gravar o comando (como as issues #5/#40).
Diagnóstico: `TOTK_CRUMBS_OPS=1` (marcador antes de cada op NVN, início/fim de passe e etapas do present; `vk_crumbs.c`).
Autoplay sem jogador: `TOTK_INPUT_SCRIPT=build/smo-v141/autoplay.txt`. Depois de resets da GPU o `gpu_busy_percent`
trava em 99 e o sclk em 1900 MHz mesmo sem jogo: reiniciar o PC.
**Áudio ruidoso — corrigido:** clique a cada emenda de 5 ms (aspereza 1,7× na fronteira do bloco de 240 amostras,
medida gravando o monitor do PipeWire). `audren.c advance_voice` contava as amostras consumidas por uma multiplicação e
`audio_mixer.c voice_render` por soma passo a passo: vozes não-48 kHz começavam o bloco seguinte uma amostra fora.
Agora as duas contam igual (1,2×, nível do ruído). Também entraram as rampas de volume da voz e do mix
(`accumulate_ramp`), como o DSP faz.
**Reverb granulado (também nas cavernas do TotK) — corrigido:** as linhas de atraso dos dois reverbs (`audio_effects.c`
`line_*`, `audio_reverb.c delay_*`), herdadas do Ryujinx, davam a volta num tamanho e liam as reflexões com outro: cada
reflexão lia uma casa nunca escrita uma vez por volta. Senoide de 220 Hz: falhas de 1 amostra por segundo 56,7 → 0
(I3DL2) e 234 → 0 (padrão).
**Pipocadas em pulos e vozes — corrigido:** o SMO roda 5 efeitos AUX (tipo 2: o atk processa na CPU e devolve por
um anel de retorno; o TotK usa os efeitos nativos). O render, ditado pelo dispositivo (PipeWire pede 1024 amostras de uma
vez), fazia 4–5 blocos em rajada, e o jogo não preenchia o retorno a tempo: líamos amostras velhas, um estalo por emenda
(20–30/s em cena cheia, medido com `TOTK_AUDIO_DUMP`). Agora os blocos saem com pelo menos 4 ms entre si
(`audren.c render_thread`): 1,9/s, o jogador não ouve mais. Também entraram: prefill de 60 ms no SMO (o stream tinha
xruns com 20 ms), o depop do DSP e `TOTK_AUDIO_DUMP=<arquivo>` (mix float32 antes do clamp).
**Bloom piscando e quadrado (2026-11-03): é do jogo.** O passe de máscara do bloom (agl bloom_mask, fs
f529eac42e6c748c) desenha 1/16 da cena (100x56 de 1600x900) com uma amostra por pixel e LOD implícito, e a cena tem um
nível só: luz pequena distante entra e sai do pixel da máscara. O console faz igual (o usuário confirmou). Melhoria:
`TOTK_SMOOTH_BLOOM` (padrão ligado, ao vivo, menu "Smooth bloom"): a máscara lê um "mip twin" da cena com a cadeia de
mips inteira (`vk_exec_draw.c` mtwin_update), e o LOD implícito pega a média. É uma intensidade de 0 a 3 (0 = o
jogo; 2 e 3 = bias de LOD +1 e +2 no sampler). O antigo `TOTK_BLOOM_OFF` saiu; `smo_bloom_keys.inc` (cada shader com
o efeito de origem) fica para achar a máscara (`fx_seed_of`).
**Bloom quadrado / tela estourando para branco em algumas sessões (corrigido 2026-11-03):**
`nvnSamplerBuilderSetDefaults` zerava só os 52 bytes de `samp_builder_t`, e o cache de samplers do agl
(main+0x980e20) faz hash dos bytes 8..0x60 do builder. O lixo da pilha (dependia do que rodou antes: assistir a intro
da fase quebrava, pular não) mudava o hash, o cache nunca acertava, registrava ~40 samplers por frame até esgotar os
slots e então devolvia o slot 0 (`f_7000980e20` devolve 0 com o anel cheio): a cadeia do bloom ficava sem filtro e sem
clamp de LOD, lia o nível que escrevia e realimentava até estourar. Agora o builder inteiro (0x60) é zerado. O pulo de
brilho de 1 frame (o slot do passe 100x56 -> 50x28 vindo com `lod 0..14`) era o anel girando rápido pelo mesmo motivo.
**Antes:** brilho (bloom) das luzes piscando. FMZ descartado (2 de 858.551 FMUL/FFMA nos shaders do SMO).
Brilho piscando, 2026-11-01 (ferramentas NÃO commitadas no working tree: F9 dump `TOTK_DUMP=key`, F6/F7 câmera
lenta, `TOTK_INVAL_DUMP`, `TOTK_READ_NO_PRESENT_DRAIN`, log de invalidates sob `TOTK_TRACE=gfx` — remover antes do commit):
é um salto GLOBAL de um frame (tela toda +10–30% de brilho/névoa), quase sempre nos frames em que o jogo invalida as
tabelas de 128 KB lidas pela CPU (buffer duplo 0x1d7387000/0x1d6965000, a cada 2 frames). Descartado: conteúdo dessas
tabelas (suave, sem NaN/zeros) e a espera da apresentação no guest_read. Pista aberta: 0x1d8476000 (rgba16f 128x128,
render target do pass 46, lido a cada frame) e 0x1e409f000 têm checksum SEMPRE igual — conferir se a cópia de volta
dessas imagens acontece (`vk_be_guest_read` → `vk_texture_cpu_stale`).
**Backports do TotK, 2026-11-02** (commits no `smo`, base upstream/dev 49c19b2; build e selftest ok, jogo não testado):
gravador (`90a3b07` objeto adiado leva o carimbo da submissão; `328589a` `TOTK_REC_CHECK=1` / `TOTK_REC_DELAY_US`
para achar objeto reciclado que o gravador ainda nomeia — usar para retestar o travamento com `TOTK_VK_RECORDER=1`),
`dbe8daf` (shaders em compilação durante um crash são pulados no próximo início), kernel (`0ab16c2` SignalToAddress,
`1f824a6` cancel pendente no WaitSynchronization, `7c1cd42` evento de sistema religado, `cacbdf2` saída de thread sem
longjmp), memória/texturas (`9d95cbd`, `f4f9d6d`, `da94604`, `b6ab660`, `f3ce186`, `4543036`, `53d3f8e` offset
unsigned do loader 1.2.1), `984c9bc` gradientes do TXD por coordenada (mip certo), `ff5706c`, `c79b5f6`, `526e9f3`,
`cc4572b`. Pista para o brilho piscando: `f3ce186`/`4543036` mexem justamente no rastreio de escrita de textura.
Não trazido: `710b7f5` (marcas de passe do TotK usam as words 2/3 do buffer de breadcrumbs, que o `TOTK_CRUMBS_OPS`
do SMO já usa por op).
**Acima de 60 fps:** não suportado no SMO (sem tabela de patches de frame rate; o ritmo segue o vsync de 60 Hz).
Dump de frame: `TOTK_DUMP=1500 TOTK_DUMP_DIR=$PWD/build/smo-v141/dump` (pass_0000 = menu correto; pass_0001 = preto).
**Bug atual:** o último passe (cópia rgb10a2 → rgba8srgb 0x144800000, 1 draw, vs 0744b810fbe3e242 / fs 3444fa67f4a6dd2e)
sai todo zero (alfa também). O fs só amostra a textura certa (tex 282 = alvo do pass 0). O vs calcula a posição com
uma **matriz de um uniform buffer do jogo** × atributo 0: se o cbuf chega zerado, os 3 vértices colapsam e nada é
desenhado. `TOTK_PIPE_SKIP=none` não muda. Próximo: despejar o cbuf/vertex buffer desse draw (gdb em
`nvnp_nvnCommandBufferBindUniformBuffer`/`BindVertexBuffer`, ou `TOTK_DUMP_BUF`) e ver se é snapshot de memória
(vk_usnap) ou layout de binding do SDK 7.

## Próximo
1. Corrigir o passe final (acima) → item F4 frame completo; depois validar a tela de título.
2. Firmware do usuário (opcional): `tools/extract_fonts.py` para fontes reais.
3. Pendências: `frame_rate.c player_pos`/`resolution.c`/`swkbd.c` com constantes do TotK; `--seconds` usa o relógio
   do mundo do TotK (no SMO nunca dispara); renomear binário para `smo`; alias `SMO_*` em `cfg.c`; sync com upstream.

## Bloqueios
- Nenhum (firmware opcional: fontes livres funcionam).

## Crash conhecido (2026-11-02)
`FATAL: access violation at smo+0x4f69099, reading 0x1db204ea4`, depois de uns 5 min (frame ~19800), com o menu aberto:
chamada indireta para `x8 = 0x70200015b0` vinda de `main+0x9422a0`; pilha main+0x625724 <- main+0x964640 <-
sdk+0x329e88 (início de thread). Já existia antes dos patches do SMO (nenhum conjunto ligado nesse run).

## Sombras verdes / luz indireta escura (resolvido, 2026-11-03)
Sintoma: tudo o que estava na sombra (paredes, prédios, sombras dinâmicas do Reino da Areia) ficava verde-oliva e
escuro; no Power Moon Recomp e no console fica azulado e claro.
Causa: o filtro das sondas de luz (passe que gera o cubo rgba8 de cada sonda na carga da área, fs 18db8d4f67f421da)
amostra o céu como cubo a partir de um array 2D BC3 de 6 camadas (128x128, 8 níveis). A imagem não era criada
CUBE_COMPATIBLE (só alvos CUBEMAP eram), então `vk_exec_draw.c get_view` não dava a vista de cubo e o shader lia a
textura substituta preta. Sem o céu, a luz indireta ficava só com a luz de preenchimento (0.452, 1.0, 0) x 21.2, que
é verde mesmo nos dados da fase (o Power Moon recebe os mesmos uniforms).
Correção: o array ganha um "cube twin" (`vk_exec_draw.c` ctwin_update): uma imagem CUBE_COMPATIBLE do mesmo formato,
tamanho, níveis e camadas, copiada do array na primeira leitura como cubo e de novo quando o contador de conteúdo
(`VkTexImage.cgen`, `vk_texture.c`) muda. A imagem original não muda, então vale para todos os drivers. Numa partida de
13.200 frames foram 10 cópias, todas em cargas de área. TOTK_CUBE_TWIN=0 desliga.
Ferramentas de diagnóstico (sem commit, no working tree): TOTK_POKE (find/peek/hold/dump/dumplog ao vivo),
TOTK_DUMP_LOG_CUBES, TOTK_OCCLUSION_VISIBLE, TOTK_WATCH, o log de registro de cubemaps.
