# CodeGenies: Equipe de Desenvolvimento de Software em Grafo de LLMs

Este é um projeto desenvolvido com a finalidade de criar uma plataforma baseada em linguagem natural que permita às equipes de desenvolvimento trabalharem de forma eficiente, integrando inteligência artificial para automatizar as atividades do desenho de arquitetura, desenvolvimento de código e testes.

## Requisitos

- Python 3.11 (Testado com Python 3.11.9)
- Agentes LLMs instalados localmente com Ollama (Codegemma, Mistral, Llama-3)

## Configuração do Projeto

Para configurar este projeto é necessário executar o seguinte:

1. Crie uma pasta com o nome do seu projeto e execute este arquivo `main.py` passando como parâmetro o nome do seu projeto e a localização de um arquivo chamado `project.properties`.
2. O arquivo `project.properties` pode ser criado utilizando um editor de texto, com os seguintes campos:
    ```
    # Título e Descrição do Projeto
    title=
    description=
    author=

    # Detalhamento técnico Completo do Projeto
    technical_details=

    # Tecnologias usadas nas camadas do projeto
    backend_technology=
    frontend_technology=
    ```
3. Crie novos agentes na pasta `agents` conforme a necessidade dos seu projeto para realizar tarefas diversificada como gerar arquivos de estrutura, pastas ou arquivos de código.
4. Instale o modelo desejado para cada um dos agentes em uma máquina separada (em serviços externos como Hugging Face e Ollma Library).
5. Certifique-se que as portas utilizadas por esses modelos estão abertas no seu firewall ou router, de outra forma não haverá comunicação entre os agentes.

## Execução do Projeto

Para executar o projeto siga estas etapas:

1. Dê início aos serviços externos ou modelos instalados localmente.
2. Execute este arquivo `main.py` passando como parâmetro o nome do seu projeto e a localização do arquivo `project.properties`.
3. O sistema começa a funcionar gerando os relatórios iniciais para cada um dos agentes e começando a gerar a estrutura de pastas e códigos conforme as respectivas backlogs de atividades gerados pelo analista.
4. Os desenvolvedores trabalharão em suas pastas separadas no projeto e implementarão seus códigos seguindo os passos dados nos backlogs.
5. O tester deve fazer os testes e adicioná-los a sua pasta separada, também dentro do projeto.
6. A equipe deve trabalhar em conjunto para realizar os testes no código produzido e corrigir os eventuais erros encontrados.
7. Quando estiver pronto o sistema gera o relatório completo com as informações dos agentes e os resultados dos testes realizados pelo tester.
8. É possível retornar ao início do projeto para atualizar as informações, backlogs e relatórios gerando uma nova estrutura de arquivos conforme necessário.
