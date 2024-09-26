import importlib
import inspect
import os
class PluginInterface:
    def run(self, code):
        raise NotImplementedError("Этот метод должен быть переопределен в плагине")
        
        
class PluginManager:
    def __init__(self):
        self.plugins = []
    
    def register_plugin(self, plugin: PluginInterface):
        self.plugins.append(plugin)
    
    def run_plugins(self, code: str) -> bool:
        for plugin in self.plugins:
            if not plugin.run(code):
                return False
        return True
    
    def load_plugins(self, plugins_folder='plugins'):
        for file in os.listdir(plugins_folder):
            if file.endswith(".py"):
                module_name = file[:-3] 
                module = importlib.import_module(f"{plugins_folder}.{module_name}")
                # print(module)
                # Searching subclasses of PluginInterface
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # print(obj)
                    if issubclass(obj, PluginInterface) and obj is not PluginInterface:
                        # print(f"Регистрация плагина: {name}")
                        self.register_plugin(obj())
