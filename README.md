# AutoGitCloneTool

Ferramenta para clonar repositórios de um usuário ou organização.

## Download

Você pode executar a ferramenta utilizando o código fonte e o interpretador python (será necessário instalar),
ou usar as ferramentas pré compiladas:

- [Ubuntu x64]()
- [Windows10 x64]()

## Configuração

Você precisará deixar junto com seu executável um arquivo de configuração com o nome de `config` (obrigatoriamente esse nome)
Este arquivo precisa conte os campos de `tipo de conjunto`, `nome do conjunto`, `token de autenticação`. Estes campos devem ser separados por `;`, como no exemplo abaixo:

```
user;williampilger;ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK
org;authentyAE;ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK
org;isDesign-Softwares;ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK
```

Repare que acima, estão configurados três conjuntos de dados.
Na primeira linha temos um usuário (por isso `user` como primeiro campo).
`williampilger` é o nome do usuário do qual serão baixados os dados.
`ghp_Lylsz84J4f9lMEUCt6AhirgYGYvfYkgC57CK` é o token de autenticação criado nas configurações do github.
