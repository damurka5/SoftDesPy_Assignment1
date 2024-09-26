import sys
from io import StringIO
import importlib
import inspect
# The code with timeout decorator was taken from 
# https://sky.pro/wiki/python/ustanovka-taymauta-na-vypolnenie-funktsii-v-python/
from functools import wraps
import signal
import errno
import os
from threading import Timer
from plugins_interface import PluginInterface, PluginManager

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError('Превышено время выполнения!')

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  
            return result

        return wrapper
    return decorator
### end of open-source code


user_stats = {} # dict with statistics about solved tasks, number of attempts, errors
#  {
#     user_name: {
#         tasks: [task_id],
#         attempts_for_each_task : {task_id: int}
#     }
# }

def counter(func):
    def wrapper(*args, **kwargs):
        user_name = kwargs['user_name']
        if user_name in user_stats:
            user_stats[user_name]['tasks'].append(kwargs['task_id'])
            user_stats[user_name]['attempts_for_each_task'][kwargs['task_id']] += 1
        else:
            user_stats[user_name] = {
                'tasks':[kwargs['task_id']],
                'attempts_for_each_task':{
                    kwargs['task_id']:1
                }
            }
        return func(*args, **kwargs)
    return wrapper
        


class Test:
    def __init__(self, io_file):
        self.file = io_file
        self.ins, self.outs = self.read_file(io_file)
        
    def read_file(self, file_name):
        ins = []
        outs = []
        with open(file=f'tasks/test/{file_name}') as f:
            f_str = f.read()
            f_splitted = f_str.split('-----')
            for test in f_splitted:
                input_str = test.split('___OUT___')[0].split('___IN___')[-1]
                input_out = test.split('___OUT___')[1]
                ins.append(input_str)
                outs.append(input_out)
        return ins.copy(), outs.copy()

class Task:
    def __init__(self, file_name):
        self.description = self.read_file(file_name)
        
    def read_file(self, file_name):
        with open(file=f'tasks/description/{file_name}') as f:
            return f.read()
        
class TaskChecker:
    def __init__(self, file_name, solution):
        self.task = Task(file_name=file_name)
        self.tests = Test(io_file=file_name)
        self.solution = solution
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        
    @counter    
    def run_tests(self, user_name='None', task_id=-1):
        if not self.plugin_manager.run_plugins(self.solution):
            print('Код не прошел проверку плагинов.')
            return
        
        for i, test in enumerate(zip(self.tests.ins, self.tests.outs), 1):
            print(f'Тест {i} проверяется')
            
            student_out = self.exec_to(code=self.solution, input_data=test[0].strip())
            if 'Ошибка при выполнении кода:' in student_out:
                print('Превышено время выполнения!')
                return
                
            if student_out.strip() == test[1].strip():
                print(f'Тест пройден')
                continue
            else:
                print(f'Ошибка на тесте {i}')
                return
        print('Все тесты пройдены успешно!')
        
    @timeout(seconds=2)
    def exec_to(self, code, input_data):
        original_stdout = sys.stdout
        original_stdin = sys.stdin
        
        redirected_output = sys.stdout = StringIO()
        sys.stdin = StringIO(input_data)
        
        try:
            exec(code)
            redirected_output = sys.stdout.getvalue().strip()
        except Exception as e:
            return f"Ошибка при выполнении кода: {e}"
        finally:
            sys.stdout = original_stdout
            sys.stdin = original_stdin
            
        return redirected_output
            
    
if __name__ == '__main__':
    solution = '''
a = int(input())
b = int(input())
import os
print(a+b) 
    '''
    check = TaskChecker('0_01.txt', solution=solution)
    check.run_tests(user_name='None', task_id=-1)