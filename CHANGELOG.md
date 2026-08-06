# Changelog

Todas as alterações relevantes do projeto serão documentadas nesse arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
e este projeto adota o [Versionamento Semântico (inglês)](https://semver.org/spec/v2.0.0.html).

<!--
Os tipos de alterações

- Adicionado : para novos recursos;
- Alterado : para mudanças na funcionalidade existente;
- Obsoleto : para recursos a serem removidos em breve;
- Removido : por enquanto recursos removidos;
- Corrigido : para quaisquer correções de erros;
- Segurança : em caso de vulnerabilidades;
-->

## [Não Lançado]

## [v1.4.0] - 2026-08-06

### Adicionado

- As escolhas de tema e idioma agora são guardadas e restauradas na próxima execução do aplicativo.
- Barra de rolagem na lista de PDFs carregados, com suporte à roda do mouse; antes, com muitos arquivos, os últimos ficavam fora da janela e inacessíveis.
- Integração contínua no GitHub Actions executando os testes a cada push.
- Novo arquivo `pyproject.toml` com os metadados do pacote, permitindo instalar o aplicativo via pip.
- Testes automatizados com [pytest](https://pypi.org/project/pytest/) para a validação de PDFs, os idiomas, as preferências e o fluxo de junção.

### Alterado

- Ano do copyright unificado nos metadados do executável Windows.
- As dependências foram separadas entre execução (`requisitos.txt`) e desenvolvimento (`requisitos-dev.txt`).
- Atualizadas as dependências para versões compatíveis com o Python 3.14.
- O build passou a usar `--collect-data` para o tema Sun Valley, dispensando o caminho fixo da versão do Python nos comandos.
- Substituída a biblioteca PyPDF2 (descontinuada) pela sua sucessora [pypdf](https://pypi.org/project/pypdf/).

### Removido

- Textos de idioma que não eram usados pela interface.

### Corrigido

- Apóstrofos do idioma italiano e erros de digitação em textos, comentários e README.
- A validação de PDFs agora trata arquivos ilegíveis (sem permissão de leitura, por exemplo) como inválidos em vez de fechar o aplicativo.
- A janela de salvamento agora retorna apenas o caminho escolhido em vez de abrir e esvaziar o arquivo de destino antes da escrita, o que deixava um arquivo vazio para trás em caso de erro.
- O logo e o ícone agora são localizados a partir do diretório do código; antes, executar o programa de outro diretório impedia o carregamento deles.
- O aplicativo não fecha mais silenciosamente ao juntar quando um PDF foi apagado, movido ou corrompido após o carregamento, ou quando o destino não pode ser escrito; agora uma mensagem de aviso é exibida.

## [v1.3.0] - 2025-09-30

### Adicionado

- Adicionada a funcionalidade de carregar múltiplos arquivos PDF.
- Adicionado Sun Valley via PIP.
- Adicionado arquivos PDFs inválidos para testes.
- Adicionado o arquivo de licença para uso da comunidade da UFRGS e externa.
- Adicionado o idioma espanhol.
- Adicionado os botões para alterar a ordem dos PDFs ou remover.
- Criada a pasta assets para as imagens do programa.
- Novas imagens de demonstração do programa.
- Novo arquivo `CHANGELOG.md` para as alterações do projeto.
- Novos textos para PDFs inválidos.

### Alterado

- Adicionadas anotações para os objetos.
- Ajuste no README para centralizar as imagens.
- Ajustes nos comentários do código e no README.
- Alterador o link do projeto para o repositório da UFRGS.
- Arquivos PDFs movidos para uma pasta própria.
- Atualizado os requisitos com `sv_ttk`.
- Atualização do `README.md` com as instruções de uso e descrição do projeto.
- Aumentado o tamanho máximo vertical da janela.
- Códigos do pyinstaller atualizados em README.md.

### Removido

- Arquivos desnecessários apagados.
- Removida a opção de carregar apenas um PDF.
- Removida a pasta de tema, agora é instalada junto com PIP.

## [v1.2.0] - 2024-11-07

### Adicionado

- Adicionado arquivo de especificação do build.
- Adicionado o tema [Sum Valley](https://pypi.org/project/sv-ttk/) ao projeto para compatibilidade com pyinstaller.
- Adicionado os idiomas alemão e italiano.
- Botões de Ajustes e Sobre no topo da janela (substituindo o Menu).
<!-- - Easter egg no código fonte. -->

### Alterado

- Ajuste ao importar pywinstyles.
- Ajustes na documentação e nomes dos objetos.
- Ajustes na versão e links das imagens.
- Arquivos do projeto movidos para uma pasta dedicada.
- Atualização das dependências.
- O aplicativo passa a ter apenas dois temas, claro e escuro.
- O fundo da janela principal tem seu tema alterado junto com os Widgets.

### Removido

- Conteúdo dos scripts de setup movidos para README e seus arquivos foram removidos.
- Removido o Widget de Menu.

### Corrigido

- Corrigido um bug ao carregar algum PDF.
- Corrigido um problema no tema [Sum Valley](https://pypi.org/project/sv-ttk/) que o impedia de ser usado com pyinstaller.
- Corrigido um problema que não alterava o tema da janela no Windows.

## [v1.0.2] - 2024-10-30

### Adicionado

- Adicionado um botão para remover o Frame (não implementado).
- Arquivo com a lista de ignorados pelo Git.
- Arquivos arq1.pdf e arq2.pdf para testes.
- Arquivos de requisitos.
- Arquivos para setup em sistemas Windows e Unix.
- Criadas as caixas de mensagens.
- Criado método para juntar os PDFs.
- Finalizada as traduções faltantes.
- Janela de Sobre usa um TopLevel para mostrar as informações.
- Nova imagem do CPD da UFRGS.
- Nova opção de trocar o tema do aplicativo.
- Novas traduções para a janela Sobre.
- Novo módulo para suporte a vários idiomas.
- Novo ícone da UFRGS para a aplicação.
- Primeira versão do `README.md`.
- Primeira versão em CLI.
- Textos da aplicação tem origem do arquivo de idiomas.
- Uso de um arquivo dedicado para os dados do projeto.
- Uso do Menu para troca de idiomas.
- Uso do Pillow para tratar as imagens.

### Alterado

- A ordem para remoção dos arquivos PDFs respeitará a FILO (First In, Last Out).
- A tradução é gerenciada por uma classe em vez de dicionário.
- Ajustes na barra de menu para o Sobre.
- Ajustes na tradução.
- Ajustes no conteúdo da janela Sobre.
- Atualização das dependências.
- Diversos ajustes no código.
- Novos nomes para os arquivos de setup.
- Por conta do hífen, ele foi substituído no nome do programa por sublinhado.
- Projeto convertido para POO.
- Troca dos Widgets Button, Entry, Frame e Label para ttk.
- Versão GUI da aplicação no lugar da CLI.

### Removido

- Opção de remoção de frame individual.
- Removidos textos não mais usados.

### Corrigido

- A forma de carregar um PDF não apaga mais o conteúdo.
- Corrigido o problema do PDF sendo apagado ao salvar por cima.
- Corrigido um problema que impedia a janela Sobre de exibir seu conteúdo.

### Segurança

- Desativado os campos de Input para não quebrar o programa ao buscar arquivos com nomes diferentes dos selecionados.

[Não Lançado]: https://github.com/ufrgs/pdf_merge/compare/v1.4.0...HEAD
[v1.4.0]: https://github.com/ufrgs/pdf_merge/compare/v1.3.0...v1.4.0
[v1.3.0]: https://github.com/ufrgs/pdf_merge/compare/v1.2.0...v1.3.0
[v1.2.0]: https://github.com/ufrgs/pdf_merge/compare/v1.0.2...v1.2.0
[v1.0.2]: https://github.com/ufrgs/pdf_merge/releases/tag/v1.0.2
