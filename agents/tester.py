"""
tester.py

This file defines the Tester agent class.
The class inherits from the base class defined in `base_agent.py` and
implements specific methods for its tasks.

Classes:

- Tester: Agent class (Tester).
  - __init__(self, llm, interactive=True): Initializes the agent.
    - llm (Ollama): Language model to be used by the agent.
    - interactive (bool): Defines if the process will be interactive.

"""
from agents import Developer
from main import translate_string

class Tester(Developer):
    def __init__(self, name, llm, language, interactive):
        """
        Initializes the Tester agent.            
        """
        super().__init__(name, llm, language, interactive)

    def develop_tests(self, prompt):
        tests = self.evaluate(prompt)
        if self.interactive:
            final_tests = self.interact(tests)
        else:
            final_tests = tests
        return self._parse_tests_response(final_tests)
    
    def _parse_tests_response(self, response):
        if isinstance(response, str):
            translated_code_key = translate_string("tester", 'translated_code_key', self.language)
            return {translated_code_key: response}
        elif isinstance(response, dict):
            return response
        else:
            translated_code_key = translate_string("tester", 'translated_code_key', self.language)
            return {translated_code_key: response}
    
    def get_source_code(self):
        # Get the source code of the base class
        # If the response is a simple string it is returned
        return super().get_source_code()