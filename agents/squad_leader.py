"""
squad_leader.py

Este arquivo define a classe para agentes Líderes de Equipe. 
A classe herda da classe base definida em `base_agent.py` e 
implementa métodos específicos para as suas tarefas.

Classes:

- Squad Leader: Classe do agente (Líder de Equipe).
  - __init__(self, model, [name], interactive=False): Inicializa o agente.
    - model (Ollama): Modelo de linguagem a ser utilizado pelo agente.
    - name (str): Nome do agente (apenas para Developer).
    - interactive (bool): Define se o processo será interativo.
"""
import os
from .base_agent import BaseAgent
import json

class SquadLeader(BaseAgent):
    """
    Inicializa o agente SquadLeader.
    Args:
        - model (Ollama): Modelo de linguagem a ser utilizado pelo líder de equipe.
        - interactive (bool): Define se o processo será interativo.
    """
    def __init__(self, llm, interactive=True):
        super().__init__("Líder de Equipe", llm)
        self.interactive = interactive

    def generate_general_report(self, analyst_report):
        """
        Gera o relatório geral do projeto.

        Args:
            - analyst_report (str): Relatório inicial gerado pelo analista.
        """
        instructions = ("Seja um bom analista de requisitos e crie um relatório bem completo."
                        "Com base no relatório do analista acima, gere um relatório geral do projeto, "
                        "abordando todos os aspectos relevantes: Backend, Frontend e Testes: classes, funções e "
                        "uso geral do framework escolhido conforme relatório acima, bem como todas as tarefas associadas."
        )
        prompt = f"{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        if self.interactive:
            final_response = self.interact(response)
        else:
            final_response = response
        return self._parse_response(final_response)

    def generate_backend_backlog(self, analyst_report):
        """
        Gera o backlog de tarefas de backend.

        Args:
            - analyst_report (str): Relatório inicial gerado pelo analista.
        """
        backend_backlog_model = """
            MODELO DE BACKLOG BACKEND

            **Criar Pastas**
            001. ##pastas/models: pasta para armazenar todos os modelos de dados do projeto.
            002. ##pastas/controllers: pasta para armazenar os controladores do projeto.
            003. ##pastas/services: pasta para armazenar os serviços do projeto.
            004. ##pastas/migrations: pasta para armazenar as migrações do banco de dados.
            005. ##pastas/repositories: pasta para armazenar os repositórios do projeto.

            **Criar Arquivos**
            001. ##models/user.model.py: arquivo para definir o modelo de dados do usuário.
            002. ##models/post.model.py: arquivo para definir o modelo de dados da publicação.
            003. ##controllers/auth.controller.py: arquivo para controlar a autenticação do usuário.
            004. ##controllers/post.controller.py: arquivo para controlar as publicações.
            005. ##services/auth.service.py: arquivo para os serviços de autenticação.
            006. ##services/post.service.py: arquivo para os serviços de publicações.
            007. ##repositories/user.repository.py: arquivo para os repositórios de usuário.
            008. ##repositories/post.repository.py: arquivo para os repositórios de publicações.

            **Criar Classes e Funções**
            001. ##models/user.model.py:
                * classe User: para definir o modelo de dados do usuário.
                * função validateUser(): para validar os dados do usuário.
            002. ##models/post.model.py:
                * classe Post: para definir o modelo de dados da publicação.
                * função validatePost(): para validar os dados da publicação.
            003. ##controllers/auth.controller.py:
                * função login(): para realizar o login do usuário.
                * função logout(): para realizar o logout do usuário.
            004. ##controllers/post.controller.py:
                * função createPost(): para criar uma nova publicação.
                * função getPosts(): para obter todas as publicações.
            005. ##services/auth.service.py:
                * função hashPassword(): para hashear a senha do usuário.
                * função verifyPassword(): para verificar a senha do usuário.
           """
        instructions = (
            "Com base no modelo e no relatório do Analista acima,"
            "gere o backlog de atividades de backend abordando tudo o que há pra ser desenvolvido no módulo de Backend: "
            "listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto."
            "Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias."
            "Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: "
            "1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter."
            "Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
            "\nSiga o modelo co precisão."
        )
        prompt = f"{backend_backlog_model}\n\n{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        if self.interactive:
            final_response = self.interact(response)
        else:
            final_response = response
        return self._parse_response(final_response)

    def generate_frontend_backlog(self, analyst_report):
        """
        Gera o backlog de tarefas de frontend.

        Args:
            - analyst_report (str): Relatório inicial gerado pelo analista.
        """
        frontend_backlog_model = """
            MODELO DE BACKLOG FRONTEND
            
            **Criar Pastas**
            001. ##pastas/testes: pasta para armazenar todos os arquivos relacionados a testes.
            002. ##pastas/feature-tests: pasta para armazenar os testes de funcionalidade do projeto.
            003. ##pastas/unit-tests: pasta para armazenar os testes unitários do projeto.

            **Criar Arquivos**
            001. ##testes/config.js: arquivo para configurar os testes do projeto.
            002. ##feature-test/user-create.spec.js: arquivo para testar a criação de um usuário.
            003. ##feature-test/post-create.spec.js: arquivo para testar a criação de uma publicação.
            004. ##unit-test/auth.service.test.js: arquivo para testar o serviço de autenticação do projeto.
            005. ##unit-test/db.service.test.js: arquivo para testar o serviço de banco de dados do projeto.

            **Criar Classes e Funções**
            001. ##testes/config.js:
                * funcao configTest(): para configurar os testes do projeto.
            002. ##feature-test/user-create.spec.js:
                * função createUserTest(): para testar a criação de um usuário.
                * função getUserByIdTest(): para testar a obtenção de um usuário por ID.
            003. ##feature-test/post-create.spec.js:
                * função createPostTest(): para testar a criação de uma publicação.
                * função getPostsByUserTest(): para testar a obtenção de postagens por usuário.
            004. ##unit-test/auth.service.test.js:
                * função loginTest(): para testar a autenticação do usuário.
                * função logoutTest(): para testar o logout do usuário.
            005. ##unit-test/db.service.test.js:
                * função connectToDBTest(): para testar a conexão com o banco de dados.
                * função disconnectFromDBTest(): para testar o desligamento da conexão com o banco de dados.
            """
        instructions = (
            "Com base no modelo e no relatório do Analista acima,"
            "gere o backlog de atividades de frontend abordando tudo o que há pra ser desenvolvido no módulo de Frontend: "
            "listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto."
            "Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias."
            "Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: "
            "1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter."
            "Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
            "\nSiga o modelo co precisão."
        )
        prompt = f"{frontend_backlog_model}\n\n{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        if self.interactive:
            final_response = self.interact(response)
        else:
            final_response = response
        return self._parse_response(final_response)

    def generate_test_backlog(self, analyst_report):
        """
        Gera o backlog de tarefas de testes.

        Args:
            - analyst_report (str): Relatório inicial gerado pelo analista.
        """
        tests_backlog_model = """
            MODELO DE BACKLOG DE TESTES

            **Criar Pastas**
            001. ##pastas/unit-tests: pasta para armazenar os testes unitários do projeto.
            002. ##pastas/integration-tests: pasta para armazenar os testes de integração do projeto.
            003. ##pastas/e2e-tests: pasta para armazenar os testes de ponta a ponta do projeto.
            004. ##pastas/mocks: pasta para armazenar mocks e stubs usados nos testes.
            005. ##pastas/utils: pasta para armazenar utilitários e helpers para os testes.

            **Criar Arquivos**
            001. ##unit-tests/auth.service.test.js: arquivo para testar o serviço de autenticação do projeto.
            002. ##unit-tests/user.service.test.js: arquivo para testar o serviço de usuário do projeto.
            003. ##integration-tests/auth.integration.test.js: arquivo para testar a integração do serviço de autenticação com o banco de dados.
            004. ##integration-tests/user.integration.test.js: arquivo para testar a integração do serviço de usuário com o banco de dados.
            005. ##e2e-tests/login.e2e.test.js: arquivo para testar o fluxo completo de login do usuário.
            006. ##e2e-tests/user-registration.e2e.test.js: arquivo para testar o fluxo completo de registro de usuário.
            007. ##mocks/auth.mock.js: arquivo para armazenar mocks do serviço de autenticação.
            008. ##mocks/user.mock.js: arquivo para armazenar mocks do serviço de usuário.
            009. ##utils/test-helpers.js: arquivo para armazenar helpers e utilitários para os testes.

            **Criar Classes e Funções**
            001. ##unit-tests/auth.service.test.js:
                * função loginTest(): para testar a autenticação do usuário.
                * função logoutTest(): para testar o logout do usuário.
            002. ##unit-tests/user.service.test.js:
                * função createUserTest(): para testar a criação de um usuário.
                * função getUserByIdTest(): para testar a obtenção de um usuário por ID.
            003. ##integration-tests/auth.integration.test.js:
                * função authDBConnectionTest(): para testar a conexão do serviço de autenticação com o banco de dados.
            004. ##integration-tests/user.integration.test.js:
                * função userDBConnectionTest(): para testar a conexão do serviço de usuário com o banco de dados.
            005. ##e2e-tests/login.e2e.test.js:
                * função userLoginFlowTest(): para testar o fluxo completo de login do usuário.
            006. ##e2e-tests/user-registration.e2e.test.js:
                * função userRegistrationFlowTest(): para testar o fluxo completo de registro de usuário.
            007. ##mocks/auth.mock.js:
                * função getAuthMock(): para retornar um mock do serviço de autenticação.
            008. ##mocks/user.mock.js:
                * função getUserMock(): para retornar um mock do serviço de usuário.
            009. ##utils/test-helpers.js:
                * função setupTestEnv(): para configurar o ambiente de testes.
                * função tearDownTestEnv(): para desmontar o ambiente de testes.
            """
        instructions = (
            "Com base no modelo e no relatório do Analista acima,"
            "gere o backlog de atividades de testes abordando tudo o que há pra ser desenvolvido no módulo de Testes: "
            "listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto."
            "Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias."
            "Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: "
            "1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter."
            "Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
            "\nSiga o modelo co precisão."
        )
        prompt = f"{tests_backlog_model}\n\n{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        if self.interactive:
            final_response = self.interact(response)
        else:
            final_response = response
        return self._parse_response(final_response)

    def _parse_response(self, response):
        # Se a resposta for uma string simples, apenas retorne-a
        if isinstance(response, str):
            return {"Relatório Geral": response}
        # Se for um dicionário JSON válido, retorne-o diretamente
        elif isinstance(response, dict):
            return response
        # Caso contrário, retorne um dicionário com a resposta como valor
        else:
            return {"Relatório Geral": response}
        
    def get_source_code(self):
        return super().get_source_code()  # Obtém o código-fonte da classe base
