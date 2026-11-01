# Bloqueios

## Firmware do Switch (fontes compartilhadas) — aberto em 2026-11-01
O SMO usa a fonte compartilhada do sistema (`nn::pl::GetSharedFontAddress(0)` e as outras 5) para todo texto. Ela vem
do firmware do console (system data 0100000000000810..814), que só o usuário pode fornecer.

O que fazer (qualquer um):
- Dumpar o firmware do próprio Switch (ex.: TegraExplorer/nxdumptool → pasta com os `.nca`), **ou**
- Instalar esse firmware num emulador e apontar a pasta `registered` (ex.: `~/.config/Ryujinx/bis/system/Contents/registered`).

Depois: `input.firmware = '<pasta>'` em `config.local.toml` (ou me passe o caminho).
Enquanto isso, fontes substitutas (Noto) só para desenvolvimento: elas param na lookup de um glifo que só existe na fonte real.

## Resolvidos
- (2026-11-01) vulkan-headers + vulkan-validation-layers instalados pelo usuário.
- (2026-11-01) Update correto 1.4.1 dumpado pelo usuário (o primeiro arquivo era 1.3.0).
