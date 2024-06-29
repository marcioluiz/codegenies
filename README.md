# CodeGenies: Equipe de SLMs para Desenvolvimento  de Software em Grafo de Tarefas

Este é um projeto desenvolvido com a finalidade de criar uma plataforma baseada em linguagem natural que permita às equipes de desenvolvimento trabalharem de forma eficiente, integrando inteligência artificial para automatizar as atividades do desenho de arquitetura, desenvolvimento de código e testes. O projeto faz uso de modelos de linguagem pequenos (ou SLMs como na sigla em inglês).

## Requisitos

- Python 3.11 (Testado com Python 3.11.9)
- Conda or Miniconda instalados
- Agentes SLMs instalados localmente com Ollama (Codegemma, Mistral, Llama-3)
- Framework [Langchain](https://github.com/langchain-ai/langchain) para executar os prompts nas SLMs ao percorrer o grafo de tarefas criado com a extensão [Langgraph](https://github.com/langchain-ai/langgraph)

## Configuração do Projeto

### Instalação do Ollama

1. **Baixe e instale o Ollama:**
   - Acesse o [site oficial do Ollama](https://ollama.ai) e siga as instruções para baixar e instalar o software.

2. **Configure os Modelos:**
   - Você precisará dos seguintes modelos instalados e configurados no Ollama:
     - [phi3:14b-medium-128k-instruct-q4_K_M](https://ollama.com/library/phi3:14b-medium-128k-instruct-q4_K_M) (Analyst)
     - [codegemma:7b-instruct-v1.1-q4_K_M](https://ollama.com/library/codegemma:7b-instruct-v1.1-q4_K_M) (Developer)
     - [llama3:8b-instruct-q4_K_M](https://ollama.com/library/llama3:8b-instruct-q4_K_M) (Squad Leader)
   - Caso deseje basta alterar estes nomes pelos modelos que preferir no arquivo `main.py`. Claro vc deverá baixar os modelos homônios na [Biblioteca Ollama](https://ollama.com/library/).

3. **Inicie os Modelos:**
   - Certifique-se de que os modelos estão em execução e acessíveis para que os agentes possam se comunicar com eles. Verifique as portas utilizadas e ajuste seu firewall ou roteador conforme necessário.

### Configuração do Projeto

Para configurar este projeto, siga os passos abaixo:

1. **Crie uma Pasta do Projeto:**
   - Crie uma pasta com o nome do seu projeto.

2. **Crie um Ambiente Conda para o Projeto:**
   - Crie um ambiente conda com o nome do seu projeto:
   ```
      conda create -n codegenies python=3.11
   ```
   - Execute o ambiente e confira a execução:
   ```
      conda activate codegenies
      conda info
   ```

3. **Instale as dependências do projeto:**
   - Crie um ambiente conda com o nome do seu projeto:
   ```
      pip install -r requirements.txt
   ```

4. **Configure o Arquivo `project.properties`:**
   - Utilize um editor de texto para editar o arquivo chamado `project.properties` com o seguinte conteúdo:
     ```
     # Título e Descrição do Projeto
     title=
     description=
     author=

     # Detalhamento técnico Completo do Projeto
     technical_details=

     # Tecnologias usadas nas camadas do projeto
     backend_technology=
     backend_file_extension=
     frontend_technology=
     frontend_file_extension=
     ```

5. **Inicie os Serviços Externos:**
   - Certifique-se de que os modelos instalados localmente [via Ollama Library](https://ollama.com/library/) ou em serviços externos (como [Hugging Face](https://huggingface.co/models?sort=downloads&search=gguf)) estão em execução e acessíveis para comunicar-se com o projeto. Verifique as portas utilizadas e ajuste seu firewall ou roteador conforme necessário.

6. **Execute o Script Principal:**
   - Execute o arquivo `main.py`.
   - Exemplo: `python main.py`

7. **Configure Novos Agentes:**
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

```
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
│   │   ├── relatorio_geral_do_projeto.txt
│   │   ├── backlog_de_tarefas_de_backend.txt
│   │   ├── backlog_de_tarefas_de_frontend.txt
│   │   └── backlog_de_tarefas_de_testes.txt
│   └── README.md
├── graph.py
├── LICENSE (GPL-3.0 License)
├── main.py
├── project.properties
├── README.en_US.md
├── README.md
└── requirements.txt
```

## Informações do Licenciamento

Este projeto é piblicado sob a Licença Pública Geral GNU v3.0 (GPL-3.0). Isto significa que você é livre para usar, modificar e distribuir este código, desde que respeite os termos da licença GPL. O texto completo da licença pode ser encontrado no arquivo LICENSE incluído no projeto.

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Se você tiver alguma dúvida ou encontrar problemas, abra uma issue ou envie um pull request.

---

**Aproveite a integração do uso de inteligência artificial em suas equipes de desenvolvimento com o CodeGenies!**
