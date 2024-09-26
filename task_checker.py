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
        with open(file=f'hw1/tasks/test/{file_name}') as f:
            f_str = f.read()
            f_splitted = f_str.split('-----')
            for test in f_splitted:
                input_str = test.split('___OUT___')[0].split('___IN___')[-1]
                input_out = test.split('___OUT___')[1]
                ins.append(input_str)
                outs.append(input_out)
        return ins.copy(), outs.copy()

class Task:
    def __init__(self, file_name, tests):
        self.description = self.read_file(file_name)
        self.tests = Test(file_name) 
        
    def read_file(self, file_name):
        with open(file=f'hw1/tasks/description/{file_name}') as f:
            return f.read()
        
class TaskChecker:
    def __init__(self, file_name):
        self.task = Task(file_name=file_name)
        self.test = Test(io_file=file_name)
        
    @counter    
    def run_tests(self, user_name='None', task_id=-1):
        ... # TODO code with exec
    
if __name__ == '__main__':
    print('Hey')