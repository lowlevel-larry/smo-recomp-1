# Alvo: Super Mario Odyssey 1.4.1

Gerado com `tools/smo_extract.py` + `tools/smo_target_info.py` em 2026-11-01. Hashes completos em
`tools/data/smo-expected-v1.4.1.json`.

## Identificação
| | |
|---|---|
| Título base | `0100000000010000` (v0 = 1.0.0) |
| Update | `0100000000010800`, versão de sistema v393216, **display 1.4.1** (lida do NACP do Control NCA) |
| `main` sha256 | `47ac74a66234bc1eb717b18e01fe7c880d2dd50cf1115fd046f5e5878be5f85f` |
| `main` build ID | `b424be150a8e7d78701cbe7a439d9ebf` |

**Achado:** o código (`main`, `sdk`, `subsdk0`, `rtld`) e a RomFS da 1.4.1 são **idênticos byte a byte** aos da
1.3.0 (comparado com um dump 1.3.0, v262144, que veio primeiro com o nome errado). A 1.4.1 só muda metadados. Logo:
todo conhecimento/patch de 1.3.0 da comunidade vale para a 1.4.1.

## Módulos (ExeFS 1.4.1)
| Módulo | Arquivo | Imagem | .text | Relocações | Imports / exports |
|---|---|---|---|---|---|
| main | 9.894.790 B | 0x14b1000 | 0xa2ad60 | RELA (175.957) | 702 / 44 (sem símbolos) |
| sdk | 5.310.646 B | 0xcd4000 | 0x52d880 | RELA (31.667) | 13 / 25.077 |
| subsdk0 | 3.557.941 B | 0x71d000 | 0x3732b0 | RELA (19.175) | 647 / 10.872 |
| rtld | 7.435 B | 0x4000 | 0x1a00 | RELA (34) | não é liftado |

- Só existe `subsdk0` (biblioteca de vídeo `NintendoSDK_movie`). Sem `subsdk1+`.
- **Relocação: só RELA** (sem RELR; o TotK 1.4.3 usa RELR, o loader já trata os dois).
- `main` da 1.4.1 vem **sem símbolos** (44 exports). O `main` da **1.0.0 tem 90.530 exports** com nomes: é a ponte
  para o OdysseyDecomp e para casar funções 1.0.0 → 1.4.1 (`tools/smo_addrmap.py`, F7). Base 1.0.0 extraída em
  `build/extracted/smo-v0/exefs`.

## Versões
| Item | Versão |
|---|---|
| **SDK (nnSdk)** | **7.3.2** (`NintendoSdk_nnSdk-7_3_2-Release`) — SDK de 2019; o TotK usa 20.5. Espere adaptação de layouts nos `ov_*` (os `_Static_assert` acusam). |
| **NVN** | `NintendoSDK_NVN-7_3_2`. 488 nomes `nvn*` referenciados; 462 já estão no `nvn_procs.inc` do TotK; 26 extras são NVX/internos (bootstrap, devtools, CUDA/GL interop, syncpoints, endereços reservados). |
| Middleware no main | NEX 4.6.2, libcurl/libz 7.3.2, NintendoWare Atk 7.3.2, Font 3.5.1, Vfx 3.5.1 |
| Vídeo (subsdk0) | `NintendoSDK_movie-7_3_2` |
| **audren REV** | Não é constante estática localizável; `runtime/audren.c` loga `revision_number` ao abrir o renderer. **Medir no 1º boot (F3/F5).** Pelo SDK 7.x, esperado REV6–REV7. |

## RomFS (merge base + update, 5.678.168.236 B, 4.972 arquivos)
- Extensões: `.szs` 4.666 (SARC comprimido em **Yaz0**), `.bfstm` 202, `.aras` 56, `.mp4` 44, `.bfsar` 3, `.bin` 1.
- Pastas: ObjectData 3.637, StageData 631, SoundData 267, LayoutData 215, LocalizedData 57, EventData 55,
  MovieData 44, SystemData 35, ShaderData 28, EffectData 3.
- **Vídeos: MP4** (`MovieData/`). Codec a confirmar na F5 (a lib movie do SDK 7 usa H.264; o TotK usa VP9/WebM).
