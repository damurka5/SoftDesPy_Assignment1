from plugins_interface import PluginInterface

class SecurityChecker(PluginInterface):
    def run(self, code):
        malicious_words = ['import os']
        for imp in malicious_words:
            if imp in code:
                print(f'Обнаружено небезопасное выражение: {imp}')
                return False
        return True