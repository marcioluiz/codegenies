# CodeGenies: Equipe de Desenvolvimento de Software em Grafo de LLMs

Este é um projeto desenvolvido com a finalidade de criar uma plataforma baseada em linguagem natural que permita às equipes de desenvolvimento trabalharem de forma eficiente, integrando inteligência artificial para automatizar as atividades do desenho de arquitetura, desenvolvimento de código e testes.

## Requisitos

- Python 3.11 (Testado com Python 3.11.9)
- Agentes LLMs instalados localmente com Ollama (Codegemma, Mistral, Llama-3)

## Configuração do Projeto

### Instalação do Ollama

1. **Baixe e instale o Ollama:**
   - Acesse o [site oficial do Ollama](https://ollama.ai) e siga as instruções para baixar e instalar o software.

2. **Configure os Modelos:**
   - Você precisará dos seguintes modelos instalados e configurados no Ollama:
     - `phi3:14b-medium-128k-instruct-q4_K_M` (Analyst)
     - `codegemma:7b-instruct-v1.1-q4_K_M` (Developer)
     - `llama3:8b-instruct-q4_K_M` (Squad Leader)

3. **Inicie os Modelos:**
   - Certifique-se de que os modelos estão em execução e acessíveis para que os agentes possam se comunicar com eles. Verifique as portas utilizadas e ajuste seu firewall ou roteador conforme necessário.

### Configuração do Projeto

Para configurar este projeto, siga os passos abaixo:

1. **Crie uma Pasta do Projeto:**
   - Crie uma pasta com o nome do seu projeto.

2. **Crie o Arquivo `project.properties`:**
   - Utilize um editor de texto para criar um arquivo chamado `project.properties` com o seguinte conteúdo:
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

3. **Execute o Script Principal:**
   - Execute o arquivo `main.py` passando como parâmetro o nome do seu projeto e a localização do arquivo `project.properties`.
   - Exemplo: `python main.py`

4. **Configure os Agentes:**
   - Crie novos agentes na pasta `agents` conforme a necessidade do seu projeto para realizar tarefas diversificadas, como gerar arquivos de estrutura, pastas ou arquivos de código.

## Execução do Projeto

Para executar o projeto, siga estas etapas:

1. **Inicie os Serviços Externos:**
   - Certifique-se de que os modelos instalados localmente (via Ollama) ou em serviços externos (como Hugging Face) estão em execução.

2. **Execute o Script Principal:**
   - Execute o arquivo `main.py` passando como parâmetro o nome do seu projeto e a localização do arquivo `project.properties`.
   - O sistema começará a gerar os relatórios iniciais para cada um dos agentes e iniciará a criação da estrutura de pastas e códigos conforme as respectivas backlogs de atividades geradas pelo analista.

3. **Trabalhe nos Códigos:**
   - Os desenvolvedores trabalharão em suas pastas separadas no projeto, implementando seus códigos conforme os backlogs.

4. **Teste o Código:**
   - O tester deve realizar os testes e adicioná-los à sua pasta separada, também dentro do projeto.
   - A equipe deve trabalhar em conjunto para realizar os testes no código produzido e corrigir os eventuais erros encontrados.

5. **Gere Relatórios:**
   - Quando estiver pronto, o sistema gera o relatório completo com as informações dos agentes e os resultados dos testes realizados pelo tester.

6. **Atualize o Projeto:**
   - É possível retornar ao início do projeto para atualizar as informações, backlogs e relatórios, gerando uma nova estrutura de arquivos conforme necessário.

## Estrutura de Pastas do Projeto

A estrutura de pastas do projeto será organizada da seguinte maneira:
project_name/
├── agents/
│   ├── analyst.py
│   ├── squad_leader.py
│   ├── developer_backend.py
│   ├── developer_frontend.py
│   └── tester.py
├── build/
│   ├── dev/
│   │   ├── desenvolvedor_backend/
│   │   ├── desenvolvedor_frontend/
│   │   └── tester/
│   ├── reports/
│   │   ├── relatório_geral_do_projeto.txt
│   │   ├── backlog_de_tarefas_de_backend.txt
│   │   ├── backlog_de_tarefas_de_frontend.txt
│   │   └── backlog_de_tarefas_de_testes.txt
│   └── README.md
├── project.properties
└── main.py

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Se você tiver alguma dúvida ou encontrar problemas, abra uma issue ou envie um pull request.

---

**Aproveite a integração de inteligência artificial em suas equipes de desenvolvimento com o CodeGenies!**