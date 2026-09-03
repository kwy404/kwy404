# Como colocar no ar (5 passos)

1. Crie um repositório público chamado exatamente **kwy404** (mesmo nome do usuário). O GitHub usa esse repo como README do perfil.
2. Suba todos os arquivos desta pasta na branch **main** (README.md, light.svg, dark.svg, projects.json, logos/, .github/).
3. Em **Settings > Actions > General > Workflow permissions**, marque **Read and write permissions** e salve.
4. Vá em **Actions**, rode manualmente "Generate Snake Animation" e "Generate Projects Panel" (botão *Run workflow*). Eles criam as branches `output` e `projects`.
5. Abra github.com/kwy404 e confira. As imagens carregam direto do CDN do GitHub (raw.githubusercontent.com), sem hospedagem externa.

## Editar

- Textos do header: `gen_header.py` (lista `LINES`) -> rode `python3 gen_header.py` -> gera light.svg e dark.svg de novo.
- Projetos: edite `projects.json` (nome, repo, descrição, tags) e coloque a logo em `logos/` (PNG). O painel atualiza sozinho no push.
- Cores: azul royal #2563EB, navy #1E3A8A, ciano #22D3EE. Estão no gen_header.py, no README e nos workflows.
- Troque `seu@email.com` no README e no gen_header.py.
