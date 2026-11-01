# SMO Recomp — briefing para o Claude Code

Recompilação estática de **Super Mario Odyssey** (Switch, ARM64) para executável nativo **Linux x86-64** com Vulkan,
construída em cima do [TotK Recomp](https://github.com/valentderah/totk-pc-recomp) (MIT).

Este arquivo é o ponto de partida: diz o que fazer, em que ordem, o que aproveitar do TotK Recomp e do que você
precisa. Trabalhe de forma autônoma. Não pare para perguntar: quando houver ambiguidade, escolha a opção mais
razoável, registre em `docs/smo-decisions.md` (data, decisão, motivo) e siga em frente. Pare só se faltar algo que
só o usuário pode fornecer (lista na seção 2). Mantenha o `progress.json` do dashboard sempre em dia (seção 6).

---

## 1. Alvo

- **Jogo:** Super Mario Odyssey, title ID `0100000000010000`, update `0100000000010800`.
- **Versão:** **1.4.1** (base + update 1.4.1, a última que existe). A 1.4.x saiu em 2025 para o Switch 2 (GameShare,
  HDR) e provavelmente foi compilada com um SDK bem mais novo que o da 1.3.0. Confirme mesmo assim pelo hash do
  `main` e pela string de versão do SDK dentro do NSO `sdk` (procure por `NintendoSdk_nnSdk-`), e registre em
  `docs/smo-target.md`.
- **Plataforma:** Linux primeiro (Arch/Omarchy, Hyprland/Wayland, GPU NVIDIA RTX 5050 e AMD). Windows depois,
  reaproveitando o caminho que o TotK Recomp já tem.
- **Meta de qualidade:** desempenho no nível do TotK Recomp (60 fps travados com folga, sem stutter de shader),
  porque o port de SMO que já existe roda pior que o TotK num jogo mais leve.

---

## 2. Do que você precisa (o usuário fornece)

Arquivos do jogo e chaves, todos dumpados do Switch do próprio usuário:

| O quê | Onde |
|---|---|
| Base do jogo + update 1.4.1 | `/home/rocha/Downloads/Switch Dumps/Super Mario Odyssey (Base Game) + Update 1.4.1/` |
| `prod.keys` | `/home/rocha/Downloads/Switch Dumps/prod.keys` (uma pasta acima da do jogo) |

- Os caminhos têm espaços, `(`, `)` e `+`: sempre entre aspas no shell e nos arquivos Ninja.
- Na Fase 0, liste a pasta do jogo (só nomes e tamanhos), identifique qual arquivo é a base e qual é o update (pelo
  title ID: base `0100000000010000`, update `0100000000010800`) e o formato de cada um (XCI/NSP). Se houver
  `title.keys` na pasta `Switch Dumps`, use também. Se algo vier em NSZ/XCZ, descompacte para uma pasta em `build/`
  com `nsz -D` (nunca altere os originais).
- Crie `config.local.toml` na raiz (ignorado pelo git), no formato do `config.example.toml` do TotK Recomp, com esses
  caminhos, mais a saída em `build/` e a instalação de teste em `~/Games/smo-recomp-test/`. Confira se
  `config.local.toml` está no `.gitignore` antes do primeiro commit.
- Os dumps ficam onde estão: **não copie, mova nem renomeie** nada na pasta `Switch Dumps`. Só leitura.

Sistema (Arch):

```sh
sudo pacman -S --needed clang lld ninja make sdl3 opus libvpx zstd vulkan-headers vulkan-icd-loader \
    vulkan-validation-layers shaderc spirv-tools dotnet-sdk uv git pkgconf
# VMA: AUR vulkan-memory-allocator (ou o build baixa a 3.4.0 sozinho)
```

- Kernel **6.7 ou mais novo** (o write watch usa userfaultfd + `PAGEMAP_SCAN`). Confira com `uname -r`.
- Driver Vulkan 1.3 com `VK_EXT_external_memory_host` (NVIDIA proprietário ou RADV). Confira com `vulkaninfo`.
- Ghidra com loader de Switch (opcional, para análise), `llvm-objdump`, Capstone (`uv pip install capstone`).

Se algum item faltar, gere `docs/smo-blockers.md` dizendo exatamente o que falta e pare só nessa etapa.

---

## 3. Regras invioláveis

Herde e siga o `AGENTS.md` / `CLAUDE.md` do TotK Recomp. Os pontos principais:

1. **Nada do jogo no git.** Tudo que for extraído ou gerado fica em `build/` ou `generated/`. Rode
   `python tools/check_content.py --staged` antes de todo commit e ative o hook (`git config core.hooksPath .githooks`).
   Hashes (`expected-*.json`) e endereços/words de instrução em tabelas de patch são permitidos, como no TotK.
2. **Chaves nunca aparecem** em saída, log, comando ou arquivo. Passe só o caminho do arquivo.
3. **Licenças:** só copie código MIT, BSD, ISC, zlib ou Apache-2.0, mantendo o cabeçalho e adicionando uma linha em
   `THIRD_PARTY_NOTICES.md`. yuzu, suyu e outros GPL: só leitura, para entender comportamento. O **OdysseyDecomp**
   é fonte de conhecimento (nomes, structs, endereços): não copie código dele.
4. **C gerado nunca é editado à mão.** Corrija o gerador (`recomp/`).
5. Toda mudança no lifter passa nos testes diferenciais contra o Unicorn.
6. Código, comentários e commits em inglês (convenção do upstream, facilita contribuir de volta). Os docs de
   planejamento `docs/smo-*.md` podem ficar em português.

---

## 4. Estratégia de repositório: acompanhar o upstream

O TotK Recomp anda muito rápido (centenas de commits por semana). O valor do projeto depende de **puxar as melhorias
dele continuamente**: lifter, escalonador, backend Vulkan, Linux, installer. Por isso:

- **Por enquanto não existe repo no GitHub.** Tudo é local: um repositório git na máquina do usuário com o histórico do
  upstream e um único remote, `upstream` = `valentderah/totk-pc-recomp` (só fetch). **Nunca faça push** e não crie
  repo remoto, fork, PR nem issue. Se publicar algum dia, o usuário decide e adiciona o `origin`.
- Commits locais frequentes e pequenos, na branch `smo`, com `main` espelhando o `upstream/main`. Backup é com o usuário.
- **Sync semanal** (ou antes de cada fase): `git fetch upstream`, atualize `main` e faça `git merge main` na `smo`.
  Resolva conflitos e rode os testes. Registre o commit do upstream em `docs/smo-upstream.md`.
- **Mexa o mínimo nos arquivos compartilhados.** O que é só do SMO fica em arquivos novos com prefixo `smo_`
  (`runtime/smo_*.c`, `recomp/patches-smo-v<ver>.txt`, `tools/smo_*.py`, `docs/smo-*.md`). Quando precisar mudar um
  arquivo comum, prefira um ponto de extensão (tabela, `#ifdef GAME_SMO`, parâmetro) a uma reescrita.
- **Não renomeie em massa** (`TOTK_*`, `totk.c` etc.): isso quebraria todo merge futuro. Renomeie só o que o jogador
  vê: nome do binário (`smo`), título da janela, ícone, textos do installer, nome do `.ini`. Variáveis de ambiente:
  adicione um alias `SMO_*` → `TOTK_*` em `cfg.c` em vez de trocar os nomes.
- Correções genéricas que você fizer (bug no lifter, no Vulkan, no Linux) vão em **commits separados e limpos**, para
  virar PR no upstream **quando o usuário publicar**. Por ora só liste-as em `docs/smo-upstreamable.md`.
- Meta de longo prazo, sem bloquear nada agora: depois que estiver público, sugerir ao upstream separar o núcleo genérico
  (`recomp/`, runtime sem `ov_*`/patches, `vk_*`, `platform/`, installer) em repos ou submódulos próprios, dos quais
  TotK e SMO dependem.

---

## 5. Mapa do que aproveitar do TotK Recomp

| Parte | Arquivos | Uso no SMO |
|---|---|---|
| Lifter ARM64→C | `recomp/lifter.py`, `simd_c.py`, `jumptables.py`, `flags.py`, `regs.py`, `gen.py`, `nso.py`, `module.py`, `layout.py` | **Direto.** Rode no `main`/`sdk`/`subsdk*` do SMO. |
| Mecanismo de patches | `recomp/patches.py` (`set`/`site`/`spin`) | **Direto.** Conteúdo novo em `patches-smo-v<ver>.txt`. |
| Despacho, memória, hostfn | `dispatch.c`, `memory.c`, `hostfn.c`, `host.h`, `loader.c` (RELA e RELR) | **Direto.** |
| Kernel/escalonador | `kernel.c`, `svc.c`, `ipc.c` | **Direto.** Confira o número de cores e as prioridades que o SMO usa. |
| Plataforma Linux | `platform/linux.c`, `*_sdl.c`, `gfx_window_sdl.c`, `input_sdl.c` | **Direto.** É o caminho principal. |
| Backend Vulkan | `vk_*.c`, `tex_*.c`, `vk_astc.c`, `vk_fsr.c`, `shaders/` | **Direto.** Ajustes só onde a NVN antiga diferir. |
| Front end NVN | `nvn_api_*.c`, `nvn_obj.h`, `nvn_tex.c`, `nvn_procs.*` | **Adaptar:** regenerar procs (`tools/gen_nvn_procs.py`), conferir o tamanho dos builders/objetos para a versão de NVN do SMO. |
| Tradutor de shaders | `tools/xlate/` (Ryujinx 1.3.2 + patches) | **Direto.** |
| Overrides do SDK `nn::*` | `ov_system.c`, `ov_input.c`, `ov_gfx.c`, `ov_media.c`, `fs_host.c`, `romfs.c` | **Adaptar** à versão de SDK do SMO (nomes mangled, layouts; os `_Static_assert` acusam). |
| Áudio | `audren.c`, `audio_*.c` | **Adaptar** à revisão REV do SMO (o código já ramifica por revisão). |
| Menu/overlay/config | `ui/`, `ui_text.c`, `cfg.c`, `perf*.c`, `flight.c` | **Direto**, com textos do SMO. |
| Ferramentas | `tools/extract.py`, `build_game.py`, `spin_waits.py`, `prepare_shaders.py`, `pack_shader_cache.py`, `prof_report.py`, `check_content.py` | **Direto/adaptar** (title IDs, versões). |
| Installer/launcher | `installer/`, `tools/make_release_linux.py` (AppImage), `tools/make_release.py` | **Adaptar:** title IDs, versão, textos, nome do binário. |
| Testes | `tests/` (diferencial, jumptables, installer) | **Direto.** |
| **Não serve** | `patches-v1*.txt`, `tools/data/expected-v*.json`, lista de shaders do MacNativeGames, `ov_zstd.c`, `make_romfs_patches.py`/`ultrawide_layout.py` (HUD do TotK), guard de uniform do TotK 1.2.1, seção 6 do `docs/maxwell.md` | Substituir pelos equivalentes do SMO. |

Fontes de conhecimento sobre o SMO:
- **OdysseyDecomp** (`MonsterDruide1/OdysseyDecomp`): decomp matching, focado na **1.0.0**. Dá nomes e structs de
  `al`/`sead`/`game`. Endereços da 1.0.0 precisam ser **mapeados para a versão alvo** (casamento de funções por
  bytes/assinatura; escreva `tools/smo_addrmap.py`).
- Mods de 60 fps/resolução para emulador (cheats IPS/exefs) como pista de sites de patch.
- Switchbrew e Ryujinx (MIT) para comportamento de serviços.
- Port de SMO existente (feito com "SwitchRecomp"): se o código for aberto, leia para achar armadilhas, mas não
  dependa dele.

---

## 6. Dashboard de progresso (localhost)

O usuário acompanha o projeto por um site local que mostra a **% até a primeira build jogável** e **o que o Claude
Code está fazendo agora**. Os arquivos vêm prontos na pasta `dashboard/` (entregue junto com este README):

| Arquivo | Papel |
|---|---|
| `dashboard/server.py` | servidor só com a stdlib, em `http://localhost:8787` (bind 127.0.0.1) |
| `dashboard/index.html` | a página; atualiza sozinha a cada 2 s |
| `dashboard/hook.py` | hook do Claude Code: grava cada ação sua em `dashboard/activity.jsonl` (o "Agora" e o feed) |
| `dashboard/settings.local.json` | configuração dos hooks (`PreToolUse`, `UserPromptSubmit`, `Stop`) |
| `dashboard/progress.example.json` | modelo do `progress.json`, com os 15 itens e pesos já preenchidos |

**Na Fase 0, antes de tudo:**
1. A pasta `dashboard/` fica na raiz. Ela não colide com nada do upstream, então pode continuar lá durante o checkout.
2. `mkdir -p .claude && cp dashboard/settings.local.json .claude/settings.local.json`. Se já existir um
   `settings.local.json`, faça merge da chave `hooks`. Os hooks valem a partir da próxima sessão do Claude Code: avise
   o usuário em `docs/smo-progress.md` que ele precisa reiniciar o `claude` uma vez.
3. `cp dashboard/progress.example.json progress.json`.
4. Adicione `dashboard/`, `progress.json` e `.claude/settings.local.json` em `.git/info/exclude`. Ficam fora do git
   para não sujar os merges.

**`progress.json` é sua responsabilidade. Mantenha-o sempre atualizado**: depois de cada passo concluído, de todo
commit, de todo bloqueio novo, não só no fim da fase. Campos:

- `phase`: fase atual (ex.: `"F2 · lift e link"`).
- `now`: a tarefa em que você está, numa frase (ex.: `"corrigindo LDAXP no lifter, 3 testes diferenciais falhando"`).
- `next`: o próximo passo.
- `updated`: data e hora ISO-8601 com fuso (`-03:00`).
- `blockers`: lista de frases do que depende do usuário (também em `docs/smo-blockers.md`). Vazia se não houver.
- `items[]`: o checklist. Mude só `status` (`todo` / `doing` / `done`), `partial` (0 a 0,5, só em `doing`) e `note`.
  Não mude ids, textos nem pesos.
- `log[]`: marcos curtos `{"t": "03/11 20:55", "msg": "lift completo: main, sdk, subsdk0"}`. Um por item concluído
  ou descoberta importante.

**Primeira build jogável** = o binário `smo` nativo no Linux abre, mostra a tela de título, deixa entrar no Cap
Kingdom e jogar com controle e teclado, com som, sem crash por 10 minutos.

A página calcula o percentual sozinha: soma dos pesos `done` + `peso × partial` dos `doing`. Regras de honestidade:
- `done` só com o critério verificado.
- `partial` no máximo 0,5, e só com resultado medível (ex.: "8 de 15 casos do teste passam" → 0,25).
- Nunca arredonde para cima.

| Peso | Item (id) |
|---|---|
| 3 | `f0-env` ambiente pronto, selftest e testes do lifter passam no Linux |
| 2 | `f0-repo` repo local com `upstream` e branch `smo` |
| 5 | `f1-extract` extração da 1.4.1 reprodutível + `smo-target.md` completo |
| 8 | `f2-lift` lift de todos os módulos + oráculo de cobertura 100% |
| 4 | `f2-jt` jump tables com 0 divergências |
| 6 | `f2-link` `smo` linka e `--selftest` passa |
| 5 | `f3-gap` inventário `nn::*` (`smo-sdk-gap.md`) |
| 10 | `f3-boot` boot até criar o device NVN sem `rt_fatal` |
| 5 | `f4-probes` probes de NVN/Vulkan passam com a NVN do SMO |
| 8 | `f4-frame` primeiro frame apresentado na janela |
| 12 | `f4-title` tela de título renderiza correta |
| 8 | `f5-romfs` RomFS/Yaz0 carregando os assets do Cap Kingdom |
| 6 | `f5-audio` áudio funcionando |
| 8 | `f6-input` input básico (teclado e gamepad) |
| 10 | `playable` Cap Kingdom jogável por 10 min sem crash |

Depois da primeira build jogável, troque `milestone` para "build completa", zere os itens e crie novos para as
fases 6 a 8 (pesos somando 100), registrando a troca no `log`.

O usuário sobe o site com `python3 dashboard/server.py` (num terminal separado). Não é tarefa sua manter o
servidor rodando.

## 7. Fases

Cada fase termina com: testes verdes, `check_content.py` limpo, commit, uma linha em `docs/smo-progress.md`,
`progress.json` atualizado e sync com o upstream. Use a lista de tarefas para acompanhar.

### Fase 0 — Repo e ambiente
1. Na pasta onde este README está: `git init`, `git remote add upstream https://github.com/valentderah/totk-pc-recomp.git`,
   `git fetch upstream`, `git checkout -b main upstream/main` (antes, tire este README do caminho, por exemplo para
   `../smo-plan.md`, porque o upstream tem um README). Depois `git checkout -b smo`, coloque o plano em
   `docs/smo-plan.md` e faça o primeiro commit. Não crie remote além do `upstream`.
2. `tools/fetch_refs.sh` para os refs do upstream, e clone também `OdysseyDecomp` em `refs/` (somente leitura).
3. Monte o ambiente Linux conforme `docs/building.md` → "Linux". Rode o selftest **sem arquivos de jogo** e os
   testes diferenciais do lifter.
4. Rode `tools/check_platform.py`. Deve dar 0 usos de Win32 fora da lista permitida.
- **Pronto quando:** o selftest e os testes do lifter passam no Linux do usuário.

### Fase 1 — Extração e identificação
1. Generalize `tools/extract.py` para receber o perfil do jogo (title IDs, módulos esperados) sem quebrar o TotK
   (`tools/smo_profile.py` ou tabela).
2. Extraia ExeFS/RomFS para `build/extracted/smo-v<ver>/`, com merge do update.
3. Gere `tools/data/smo-expected-v<ver>.json` (só hashes).
4. Escreva `docs/smo-target.md` com: versão, hash do `main`, módulos (`main`, `sdk`, `subsdk*`, `rtld`), tamanho,
   **versão do SDK**, **versão da NVN** (procs importados), **revisão do audren**, tipo de relocação, formato da RomFS
   (Yaz0/SZS/SARC), formato dos vídeos.
- **Pronto quando:** extração reprodutível e `smo-target.md` completo.

### Fase 2 — Lift e link
1. Rode `recomp/gen.py` nos módulos do SMO (sem `rtld`). Corrija o que faltar no lifter, com teste diferencial.
2. Escreva o oráculo de cobertura `tools/smo_scan_sites.py`: liste todo SVC, leitura de `tpidrro_el0`/`tpidr`,
   `cntpct`/`cntfrq`, uso de `x18`, janelas exclusivas (`ldxr`/`stxr`/`ldaxp`) e jump tables. O lifter tem que tratar
   100% desses sites (no TotK isso vinha do rewriter do MacNativeGames).
3. `tests/jumptables_check.py` com 0 divergências no SMO.
4. Compile e link com `tools/build_game.py`.
- **Pronto quando:** o binário `smo` linka e `--selftest` passa (layout, tabela de despacho, registro de hostfn).

### Fase 3 — Boot até a primeira chamada NVN
1. Inventário: liste os símbolos `nn::*` importados pelo `main` do SMO e compare com os `HOST_OVERRIDE` existentes.
   Gere `docs/smo-sdk-gap.md` (tem / falta / assinatura diferente).
2. Implemente o que falta em `runtime/smo_ov_*.c` (ou adapte os `ov_*` existentes com o mínimo de diff). Stubs
   explícitos com log para: nfp/amiibo, Labo VR, GameShare/GameChat (1.4.x), prepo, friends/online.
3. Rode com o trace de host ligado até o jogo criar o device NVN.
- **Pronto quando:** o jogo inicializa o SDK e chega na NVN sem `rt_fatal`.

### Fase 4 — Gráficos até a tela de título
1. Regenere `nvn_procs.inc` para a NVN do SMO e confira structs e tamanhos de builders. As probes
   (`nvn_probe.c`, `vk_exec_probe.c`, `tex_probe.c`) precisam passar.
2. Shaders: sem a lista do MacNativeGames. Grave as variantes vistas em jogo e escreva
   `tools/smo_shader_list.py` para gerar a lista da pré-compilação na instalação.
3. Use o `docs/maxwell.md` como checklist de comportamento Maxwell e anote bugs específicos do SMO numa seção nova.
- **Pronto quando:** a tela de título renderiza corretamente no NVIDIA e no RADV.

### Fase 5 — Assets, áudio e vídeo
1. Descompressor Yaz0/SZS no host: o equivalente do `ov_zstd.c`, interceptando a função de descompressão do jogo
   (`runtime/smo_ov_yaz0.c`). Meça antes e depois.
2. audren na revisão do SMO. Áudio sem estalo a 60 fps.
3. Vídeos: identifique o formato e reaproveite `ov_movie.c` (VP9/libvpx) ou adapte.
- **Pronto quando:** dá para entrar no Cap Kingdom com áudio e as cutscenes tocam.

### Fase 6 — Gameplay completo
1. Input: teclado/mouse, gamepad, **gyro** (arremesso do chapéu com movimento; já existe `motion_fusion.c`), modo 2P
   (Cappy no segundo controle), remapeamento.
2. Saves em `profile/`, sem perder compatibilidade entre versões.
3. Teste por reino. Abra issues internas em `docs/smo-bugs.md`.
- **Pronto quando:** a história principal é jogável do começo ao fim.

### Fase 7 — Desempenho e extras
1. `tools/spin_waits.py` no SMO → linhas `spin` no arquivo de patches.
2. Profiling (overlay F10, `prof_report.py`, `crit_path.py`). Compare CPU e GPU com o TotK Recomp na mesma máquina.
3. Patches (`patches-smo-v<ver>.txt`): frame rate acima de 60 (a lógica do SMO roda a 60, então vai exigir
   desacoplar o timestep, como os patches de realtime do TotK), resolução interna, aspect ratio/ultrawide e FOV,
   desligar o resolution scaling dinâmico. Sites encontrados via decomp e mapeados para a versão alvo.
- **Pronto quando:** 60 fps travados no notebook do usuário (Ryzen 7 260 + RTX 5050) e opção de >60 fps.

### Fase 8 — Installer/launcher Linux
1. Adapte `installer/` com perfil do SMO (title IDs, versão, passos, espaço em disco, textos en/pt-BR).
2. `tools/make_release_linux.py` → `SMO-Setup-x86_64.AppImage`, com o game buildado na máquina do jogador.
   Nada derivado do jogo vai no release.
3. Teste no Steam Deck se der.
- **Pronto quando:** de uma pasta vazia, o AppImage + os arquivos do usuário geram uma instalação jogável.

### Fase 9 (depois) — Windows
Reaproveite o caminho Win32 do upstream: installer `.exe` e llvm-mingw.

---

## 8. Riscos conhecidos

- **Versão do SDK:** se a 1.4.x usar SDK novo, os `ov_*` do TotK (SDK 20.5) servem mais; se for 1.3.0 (SDK de
  2019), espere mais adaptação nos layouts. O inventário da Fase 3 mede isso.
- **Decomp na 1.0.0:** os endereços não batem com a versão alvo. Sem o mapeamento da Fase 7, os patches ficam lentos.
- **Upstream rápido:** se o sync ficar mais de 2 semanas parado, o merge vira um projeto em si. Não deixe.
- **Takedown:** mantenha a fronteira de conteúdo impecável, sem assets, sem código derivado no release, com build
  local. Nome e ícone sem marcas da Nintendo no repo (use "SMO Recomp" e um ícone próprio).

---

## 9. Arquivos que você mantém

| Arquivo | Conteúdo |
|---|---|
| `progress.json` | estado do dashboard: % até a build jogável, tarefa atual, bloqueios (fora do git) |
| `docs/smo-plan.md` | este plano |
| `docs/smo-target.md` | versão, SDK, NVN, audren, formatos |
| `docs/smo-progress.md` | uma linha por fase/marco |
| `docs/smo-decisions.md` | decisões tomadas sem perguntar |
| `docs/smo-upstream.md` | commits do upstream já mergeados |
| `docs/smo-upstreamable.md` | correções genéricas para virar PR no upstream |
| `docs/smo-sdk-gap.md` | inventário `nn::*` |
| `docs/smo-bugs.md` | bugs conhecidos |
| `docs/smo-blockers.md` | o que falta do usuário (só se houver) |
