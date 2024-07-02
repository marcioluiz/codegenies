# prompt_templates/squad_leader_templates.py

class SquadLeaderPrompts:
    # Instruções de criação do backlog de atividades do backend
    # Instructions for creating the backend activity backlog
    general_report_instructions = (
        """
        Seja um bom analista de requisitos e crie um relatório bem completo.
        Com base no relatório do analista acima, gere um relatório geral do projeto, 
        abordando todos os aspectos relevantes: Backend, Frontend e Testes: classes, funções e 
        uso geral do framework escolhido conforme relatório acima, bem como todas as tarefas associadas.
        """
    )

    # Modelo de backlog backend
    # Backend backlog template
    backend_backlog_model = (
        """
        MODELO DE BACKLOG BACKEND

        **Criar Arquivos, Pastas, Classes e Funções**
        001. ##models/user.model.py: arquivo para definir o modelo de dados do usuário.
            * classe User: para definir o modelo de dados do usuário.
            * função validateUser(): para validar os dados do usuário.
        002. ##models/video.model.py: arquivo para definir o modelo de dados dos videos.
            * classe Video: para definir o modelo de dados do video.
            * função validateVideo(): para validar os dados do video.
        003. ##models/comment.model.py: arquivo para definir o modelo de dados de comentários.
            * classe Comment: para definir o modelo de dados dos comentários dos vídeos.
            * função validateComment(): para validar os dados dos comentários dos vídeos.
        004. ##controllers/auth.controller.py: arquivo para controlar a autenticação do usuário.
            * função login(): para realizar o login do usuário.
            * função logout(): para realizar o logout do usuário.
        005. ##controllers/videostream.controller.py: arquivo para controlar o stream de videos.
            * função createComment(): para criar um novo comentário.
            * função getCommments(): para obter todos os comentário.
        006. ##controllers/comment.controller.py: arquivo para controlar os comentários de vídeos.
            * função createVideo(): para criar um novo vídeo.
            * função getVideos(): para obter todos os vídeos;
            * função getVideosbyUserID(): para obter todos os vídeos de um usuário pelon seu ID;
            * função getVideosbyTag(): para obter todos os vídeos de uma determinada Tag;
        007. ##services/auth.service.py: arquivo para os serviços de autenticação.
            * função createVideoStream(): para criar uma nova transmissão de vídeo.
            * função getVideoStreams(): para obter todas as transmissões de vídeos.
            * função getVideoDetails(): para recuperar os detalhes de um vídeo.
            * função verifyVideoByID(): para verificar a existência de um vídeo por ID.
        008. ##services/video.service.py: arquivo para os serviços do video.
            * função hashPassword(): para hashear a senha do usuário.
            * função verifyPassword(): para verificar a senha do usuário.
        009. ##services/videostream.service.py: arquivo para os serviços de stream de videos.
            * função getVideoByID(): para recuperar um vídeo pelo seu ID.
            * função getVideoByName(): para recuperar um vídeo pelo seu Nome.
            * função verifyIndexFromVideo(): para verificar a existência de um índex temporal em um vídeo.
        010. ##repositories/user.repository.py: arquivo para os repositórios de usuário.
            * função getVideoStreamByID(): para recuperar os uma transmissão de vídeo a partir do seu ID.
            * função getVideoStreamByIndex(): para recuperar os uma transmissão de vídeo a partir do seu ID e um índex temporal.
        011. ##repositories/video.repository.py: arquivo para os repositórios de videos.
        """
    )

    # Instruções de criação do backlog de atividades do backend
    # Instructions for creating the backend activity backlog
    backend_instructions = (
        """
        Com base no modelo e no relatório do Analista acima,
        gere o backlog de atividades de backend abordando tudo o que há pra ser desenvolvido no módulo de Backend: 
        listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto.
        Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias.
        Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 
        1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter.
        Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext
        \nSiga o modelo com precisão. Tem que haver apenas um item superior começando com "**Criar Arquivos, Pastas, Classes e Funções**" e 
        hierarquicamente abaixo instruções que contem os nomes das pastas e arquivos na forma: "##pasta/arquivo.ext : explicação do arquivo"  em apenas uma linha
        e por fim hierarquicamente abaixo, iniciado por "*" as funções, estruturas de dados e algoritmos de cada arquivo uma instrução por linha.
        """
    )

    # Modelo de backlog frontend
    # Frontend backlog template
    frontend_backlog_model = (
        """
        MODELO DE BACKLOG FRONTEND
                
        **Criar Arquivos, Pastas, Classes e Funções**
        001. ##models/user.model.js: arquivo para definir o modelo de dados do usuário.
            * classe User: para definir o modelo de dados do usuário.
            * função validateUser(): para validar os dados do usuário.
        002. ##models/video.model.js: arquivo para definir o modelo de dados dos videos.
            * classe Video: para definir o modelo de dados do video.
            * função validateVideo(): para validar os dados do video.
        003. ##models/comment.model.js: arquivo para definir o modelo de dados de comentários.
            * classe Comment: para definir o modelo de dados dos comentários dos vídeos.
            * função validateComment(): para validar os dados dos comentários dos vídeos.
        004. ##controllers/auth.controller.js: arquivo para controlar a autenticação do usuário.
            * função login(): para realizar o login do usuário.
            * função logout(): para realizar o logout do usuário.
        005. ##controllers/comment.controller.js: arquivo para controlar os comentários de vídeos.
            * função createComment(): para criar um novo comentário.
            * função getCommments(): para obter todos os comentário.
        006. ##controllers/video.controller.js: arquivo para controlar os videos.
            * função createVideo(): para criar um novo vídeo.
            * função getVideos(): para obter todos os vídeos
        007. ##pages/usertimeline.page.js: pagina de timeline de videos do usuário.
        008. ##pages/videotimeline.page.js: pagina de timeline de videos de todos os usuários.
        009. ##pages/homepage.page.js: pagina homepara todos os usuários, contem as abas: User Timeline e Videos Timeline.
        010. ##pages/userprofile.page.js: pagina de perfil usuário.
        011. ##services/auth.service.js: arquivo para os serviços de autenticação.
            * função hashPassword(): para hashear a senha do usuário.
            * função verifyPassword(): para verificar a senha do usuário.
        012. ##services/video.service.js: arquivo para os serviços do video.
        013. ##services/comment.service.js: arquivo para os serviços de comentários.
        014. ##services/videostream.service.js: arquivo para os serviços de stream de videos.
        """
    )

    # Instruções de criação do backlog de atividades do frontend
    # Instructions for creating the frontend activity backlog
    frontend_instructions = (
        """
        Com base no modelo e no relatório do Analista acima,
        gere o backlog de atividades de frontend abordando tudo o que há pra ser desenvolvido no módulo de Frontend: 
        listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto.
        Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias.
        Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 
        1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter.
        Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext
        \nSiga o modelo com precisão. Tem que haver apenas um item superior começando com "**Criar Arquivos, Pastas, Classes e Funções**" e 
        hierarquicamente abaixo instruções que contem os nomes das pastas e arquivos na forma: "##pasta/arquivo.ext : explicação do arquivo"  em apenas uma linha
        e por fim hierarquicamente abaixo, iniciado por "*" as funções, estruturas de dados e algoritmos de cada arquivo uma instrução por linha.
        """
    )

    # Modelo de backlog de testes
    # Tests backlog template
    tests_backlog_model = (
        """
        MODELO DE BACKLOG DE TESTES

        **Criar Arquivos, Pastas, Classes e Funções**
        001. ##unit-tests/auth.service.test.js: arquivo para testar o serviço de autenticação do projeto.
            * função loginTest(): para testar a autenticação do usuário.
            * função logoutTest(): para testar o logout do usuário.
        002. ##unit-tests/user.service.test.js: arquivo para testar o serviço de usuário do projeto.
            * função createUserTest(): para testar a criação de um usuário.
            * função getUserByIdTest(): para testar a obtenção de um usuário por ID.
        003. ##integration-tests/auth.integration.test.js: arquivo para testar a integração do serviço de autenticação com o banco de dados.
            * função authDBConnectionTest(): para testar a conexão do serviço de autenticação com o banco de dados.
        004. ##integration-tests/user.integration.test.js: arquivo para testar a integração do serviço de usuário com o banco de dados.
            * função userDBConnectionTest(): para testar a conexão do serviço de usuário com o banco de dados.
        005. ##e2e-tests/login.e2e.test.js: arquivo para testar o fluxo completo de login do usuário.
            * função userLoginFlowTest(): para testar o fluxo completo de login do usuário.
        006. ##e2e-tests/user-registration.e2e.test.js: arquivo para testar o fluxo completo de registro de usuário.
            * função userRegistrationFlowTest(): para testar o fluxo completo de registro de usuário.
        007. ##mocks/auth.mock.js: arquivo para armazenar mocks do serviço de autenticação.
            * função getAuthMock(): para retornar um mock do serviço de autenticação.
        008. ##mocks/user.mock.js: arquivo para armazenar mocks do serviço de usuário.
            * função getUserMock(): para retornar um mock do serviço de usuário.
        009. ##utils/test-helpers.js: arquivo para armazenar helpers e utilitários para os testes.
            * função setupTestEnv(): para configurar o ambiente de testes.
            * função tearDownTestEnv(): para desmontar o ambiente de testes.
        """
    )

    # Instruções de criação do backlog de atividades do testes
    # Instructions for creating the testes activity backlog
    tests_instructions = (
        """
        Com base no modelo e no relatório do Analista acima,
        gere o backlog de atividades de testes abordando tudo o que há pra ser desenvolvido no módulo de Testes: 
        listar todos os arquivos e todas as classes e funções necessárias para o funcionamento completo do projeto.
        Seja bem específico e completo nesta geração, incluindo todas as pastas, arquivos, classes e funções necessárias.
        Gere um arquivo final de instruções contendo uma instrução por linha, podendo esta instrução ser de um dos dois tipos a seguir: 
        1o tipo: do tipo criar pasta e o nome da pasta na frente ou 2o tipo: do tipo criar arquivo, contendo o nome do arquivo e o detalhamento das funções que deve conter.
        Favor marcar o nome de cada arquivo com uma tag: ##nomde do arquivo: nome-do-arquivo.ext
        \nSiga o modelo com precisão. Tem que haver apenas um item superior começando com "**Criar Arquivos, Pastas, Classes e Funções**" e 
        hierarquicamente abaixo instruções que contem os nomes das pastas e arquivos na forma: "##pasta/arquivo.ext : explicação do arquivo"  em apenas uma linha
        e por fim hierarquicamente abaixo, iniciado por "*" as funções, estruturas de dados e algoritmos de cada arquivo uma instrução por linha.
        """
    )