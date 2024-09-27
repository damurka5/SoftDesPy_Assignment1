from plugins_interface import PluginInterface

class SecurityChecker(PluginInterface):
    def run(self, code):
        malicious_words = ['import os']
        is_safe = lambda code: not any(imp in code for imp in malicious_words)
        if not is_safe(code):
            print(f'Обнаружено небезопасное выражение в коде!')
            return False
        return True