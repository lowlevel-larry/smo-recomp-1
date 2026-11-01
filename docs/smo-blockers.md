# Bloqueios

Nenhum no momento.

## Resolvidos
- (2026-11-01) Fontes compartilhadas sem firmware: o `nn::fontll` do SDK 7 quer o TTF decodificado; o runtime decodifica o
  BFTTF para o SMO (`ov_system.c`) e `tools/smo_substitute_fonts.py` gera 6 fontes livres (Noto/Liberation, OFL).
  O firmware do usuário continua opcional (só fidelidade visual: `tools/extract_fonts.py`).
- (2026-11-01) vulkan-headers + vulkan-validation-layers instalados pelo usuário.
- (2026-11-01) Update correto 1.4.1 dumpado pelo usuário (o primeiro arquivo era 1.3.0).
