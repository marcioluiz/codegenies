# agents/squad_leader.py
import os
from .base_agent import BaseAgent
import json

class SquadLeader(BaseAgent):
    def __init__(self, llm, interactive=True):
        super().__init__("Líder de Equipe", llm)
        self.interactive = interactive

    def generate_general_report(self, analyst_report):
        instructions = "Seja um bom analista de requisitos e crie um relatório bem completo. Com base no relatório do analista acima, gere um relatório geral do projeto, abordando todos os aspectos relevantes: Backend, Frontend e Testes: classes, funções e uso geral do framework escolhido conforme relatório acima, bem como todas as tarefas associadas."
        prompt = f"{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        if self.interactive:
            final_response = self.interact(response)
        else:
            final_response = response
        return self._parse_response(final_response)

    def generate_backend_backlog(self, analyst_report):
        backlog_model_backend = """
            **Criar Pastas**
            1. ##pastas/models: pasta para armazenar todos os modelos de dados do projeto.
            2. ##pastas/controllers: pasta para armazenar os controladores do projeto.
            3. ##pastas/services: pasta para armazenar os serviços do projeto.
            4. ##pastas/migrations: pasta para armazenar as migrações do banco de dados.
            5. ##pastas/repositories: pasta para armazenar os repositórios do projeto.

            **Criar Arquivos**
            1. ##models/user.model.py: arquivo para definir o modelo de dados do usuário.
            2. ##models/post.model.py: arquivo para definir o modelo de dados da publicação.
            3. ##controllers/auth.controller.py: arquivo para controlar a autenticação do usuário.
            4. ##controllers/post.controller.py: arquivo para controlar as publicações.
            5. ##services/auth.service.py: arquivo para os serviços de autenticação.
            6. ##services/post.service.py: arquivo para os serviços de publicações.
            7. ##repositories/user.repository.py: arquivo para os repositórios de usuário.
            8. ##repositories/post.repository.py: arquivo para os repositórios de publicações.

            **Criar Classes e Funções**
            1. ##models/user.model.py:
                * classe User: para definir o modelo de dados do usuário.
                * função validateUser(): para validar os dados do usuário.
            2. ##models/post.model.py:
                * classe Post: para definir o modelo de dados da publicação.
                * função validatePost(): para validar os dados da publicação.
            3. ##controllers/auth.controller.py:
                * função login(): para realizar o login do usuário.
                * função logout(): para realizar o logout do usuário.
            4. ##controllers/post.controller.py:
                * função createPost(): para criar uma nova publicação.
                * função getPosts(): para obter todas as publicações.
            5. ##services/auth.service.py:
                * função hashPassword(): para hashear a senha do usuário.
                * função verifyPassword(): para verificar a senha do usuário.
           """
        instructions = "Com base no modelo e no relatório do Analista acima, gere o backlog de atividades de backend abordando tudo o que há pra ser desenvolvido no módulo de Backend: listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto. Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias. Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter. Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
        prompt = f"{backlog_model_backend}\n\n{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        if self.interactive:
            final_response = self.interact(response)
        else:
            final_response = response
        return self._parse_response(final_response)

    def generate_frontend_backlog(self, analyst_report):
        backlog_model_frontend = """
            **Criar Pastas**
            1. ##pastas/testes: pasta para armazenar todos os arquivos relacionados a testes.
            2. ##pastas/feature-tests: pasta para armazenar os testes de funcionalidade do projeto.
            3. ##pastas/unit-tests: pasta para armazenar os testes unitários do projeto.

            **Criar Arquivos**
            1. ##testes/config.js: arquivo para configurar os testes do projeto.
            2. ##feature-test/user-create.spec.js: arquivo para testar a criação de um usuário.
            3. ##feature-test/post-create.spec.js: arquivo para testar a criação de uma publicação.
            4. ##unit-test/auth.service.test.js: arquivo para testar o serviço de autenticação do projeto.
            5. ##unit-test/db.service.test.js: arquivo para testar o serviço de banco de dados do projeto.

            **Criar Classes e Funções**
            1. ##testes/config.js:
                * funcao configTest(): para configurar os testes do projeto.
            2. ##feature-test/user-create.spec.js:
                * função createUserTest(): para testar a criação de um usuário.
                * função getUserByIdTest(): para testar a obtenção de um usuário por ID.
            3. ##feature-test/post-create.spec.js:
                * função createPostTest(): para testar a criação de uma publicação.
                * função getPostsByUserTest(): para testar a obtenção de postagens por usuário.
            4. ##unit-test/auth.service.test.js:
                * função loginTest(): para testar a autenticação do usuário.
                * função logoutTest(): para testar o logout do usuário.
            5. ##unit-test/db.service.test.js:
                * função connectToDBTest(): para testar a conexão com o banco de dados.
                * função disconnectFromDBTest(): para testar o desligamento da conexão com o banco de dados.
            """
        instructions = "Com base no modelo e no relatório do Analista acima, gere o backlog de atividades de frontend abordando tudo o que há pra ser desenvolvido no módulo de Frontend: listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto. Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias. Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter. Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
        prompt = f"{backlog_model_frontend}\n\n{analyst_report}\n\n{instructions}"
        response = self.evaluate(prompt)
        if self.interactive:
            final_response = self.interact(response)
        else:
            final_response = response
        return self._parse_response(final_response)

    def generate_test_backlog(self, analyst_report):
        instructions = "Com base no relatório do Analista acima, gere o backlog de atividades de testes abordando tudo o que há pra ser desenvolvido no módulo de Testes: listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto. Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias. Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter. Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext"
        prompt = f"{analyst_report}\n\n{instructions}"
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
        
    def save_content(self, dir_path, filename, content):
        """
        Salva o conteúdo do líder de equipe em um arquivo.

        Args:
            dir_path (str): O diretório onde o arquivo será salvo.
            filename (str): O nome do arquivo.
            content (str): O conteúdo a ser salvo no arquivo.

        Returns:
            str: O conteúdo do líder de equipe.
        """
        with open(os.path.join(dir_path, filename), 'w') as file:
            file.write(content)
        
        return content
        
    def get_source_code(self):
        return super().get_source_code()  # Obtém o código-fonte da classe base
