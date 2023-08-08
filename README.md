# AutoGitCloneTool

Ferramenta para clonar repositórios de um usuário ou organização.

## Download

Você pode executar a ferramenta utilizando o código fonte e o interpretador python (será necessário instalar),
ou usar as ferramentas pré compiladas:

- [OLD VERSION - Ubuntu x64](https://github.com/williampilger/AutoGitCloneTool/raw/main/dist/GetAllRepos)
- [Windows Server x64](https://github.com/williampilger/AutoGitCloneTool/raw/main/dist/GetAllRepos.exe)

## Configuração

Você precisará deixar junto com seu executável um arquivo de configuração com o nome de `config` (obrigatoriamente esse nome).

Este arquivo precisa conte os campos de 

| **tipo de conjunto** | Função |
| --- | --- |
| `org` | Para repositórios de um usuário |
| `user` | Para repositórios de uma organização |

| **nome do conjunto** |
| --- |
| É o nome do usuário ou organização |

| **token de autenticação** |
| --- |
| Token de API do GitHub |

| **diretório de download** |
| --- |
| Diretório onde serão salvos os arquivos temporários (ou o repositório extraído, no caso do progressivo) |

| **modo de compactação** (opcional) | Descrição |
| --- | --- |
| NÃO INFORMADO | Cada vez que o backup for feito, um novo nome para o arquivo compactado é gerado. |
| `OneFile` | Todas as repetições do backup recebem o mesmo nome, e o arquivo de saída é sobrescrito/atualizado. |
| `Progressive` | O Download dos repositórios sempre será mantido, dando apenas um `git fetch` quando o mesmo já existe. | 

Estes campos devem ser separados por `;`, como no exemplo abaixo:

```
user;williampilger;ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK;down;OneFile
org;authentyAE;ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK;down
org;isDesign-Softwares;ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK;%temp%\down;Progressive
```

Repare que acima, estão configurados três conjuntos de dados.
Na primeira linha temos um usuário (por isso `user` como primeiro campo).
`williampilger` é o nome do usuário do qual serão baixados os dados.
`ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK` é o token de autenticação criado nas configurações do github.
`down` ou `%temp%\down` é o diretório, absoluto ou relativo, onde o repositório EXTRAÍDO é salvo (temporário ou definitivamente). Este campo depende do seu sistema operacional.
`OneFile` É um campo opcional, e os repositórios neste caso serão compactados sempre para o mesmo nome de arquivo, sobrescrevendo o backup anterior.


#### Criar Token de autenticação GitHub

Acesse **Seu Perfil** > **Settings** > **Developer Settings** > **Personal Access Tokens** e cadastre um novo token.



## Sobre

----------
### Compilação

As versões binparias foram compiladas com o `pyinstaller` usando:
```sh
pip install pyinstaller
pyinstaller --onefile main.py
```

**Obs.**: Se O sistema não localizar o pyinstaller, provavelmente ele não está no seu PATH.
Corrija usando:

> export PATH=$PATH:~/.local/bin

----------

By: **will.i.am** | Bom Princípio - RS
