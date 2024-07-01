# prompt_templates/developer_templates.py

develop_code_instructions = (
    "Com base no backlog de atividades acima, gere gere todo o código dos arquivos "
    "demandados nas instruções do backlog. Coloque todo o código sequencialmente marcando "
    "início de arquivos com: ##arquivo.ext eo o fim de todo arquivo com: ##end-arquivo.ext ."
)

structure_prompt_instructions = (
    "Gere a estrutura de pastas e arquivos necessária para a tarefa:"
)

code_prompt_instruction = f"Gere o código necessário para a tarefa:"

code_structure_refinement_prompt = f"observando também a estrutura criada para a mesma:"