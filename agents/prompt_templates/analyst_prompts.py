# prompt_templates/analyst_templates.py

class AnalystPrompts:
    analyst_report_prompt_instructions = (
        """
        Gere um relatório de análise do projeto completo com base nas propriedades a seguir e 
        leve cada uma delas em consideração no seu relatório:
        """
    )

    analyst_report_refinement_instructions = (
        """
        Acresente após uma análise rápida de total de pastas de módulos e 
        classes de código de no máximo 04 paragráfos ao final do relatório:
        \n[Insira aqui a análise rápida do projeto]
        """
    )