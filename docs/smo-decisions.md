# Decisões tomadas sem perguntar

| Data | Decisão | Motivo |
|---|---|---|
| 2026-11-01 | Repo em `~/projects/smo-recomp` | Padrão dos outros projetos do usuário em ~/projects. |
| 2026-11-01 | Usei o README do zip (versão com dashboard) em vez do `README (1).md` solto | É a mais nova: troca progress.txt por progress.json + site. |
| 2026-11-01 | Objetos do git puxados primeiro do clone local `~/projects/totk-pc-recomp`, depois `git fetch upstream` | Só acelera; o remote continua sendo só `upstream`. |
| 2026-11-01 | `docs/smo-handoff.md` como nota de retomada | Pedido do usuário: .md dizendo onde parou e o que falta. |
| 2026-11-01 | Versão alvo determinada pelo NACP, não pelo nome do arquivo | O arquivo "Update 1.4.1" (v262144) era 1.3.0. |
| 2026-11-01 | Suportar só a 1.4.1 | Pedido do usuário; 1.3.0 removida de build/ e tools/data. Código e RomFS de 1.3.0 e 1.4.1 são idênticos. |
| 2026-11-01 | Não extrair a RomFS base isolada | O merge com o update já gera a RomFS completa; poupa 5,7 GB. ExeFS 1.0.0 é extraído (símbolos para o decomp). |
| 2026-11-01 | `smo_extract.py` reaproveita `extract.py` e os scripts vendored trocando `program_nca` em tempo de execução | `tools/vendor/` deve ficar idêntico ao upstream; nenhum arquivo do TotK foi alterado. |
| 2026-11-01 | `excl_mt.py` (ABA) aceito como limitação conhecida do upstream | O monitor exclusivo é CAS por design; os testes diferenciais do lifter passam. |
| 2026-11-01 | `RT_SMO` via nome da build `smo-v*` (build_game.py emite `rt_game_smo`) | Ponto de extensão mínimo; nada do TotK muda de comportamento. |
| 2026-11-01 | Checkpoint SetFocusHandlingMode sem endereço exato no SMO | É alcançado por tail call; a ordem (depois dos DT_INIT) continua checada. |
| 2026-11-01 | Census de shaders do SMO em `tools/smo_shader_census.py` reaproveitando `shader_census.py` | Só o contêiner muda (Yaz0 via oead); parsers comuns ficam no upstream. |
