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
        self.tests = Test(file_name) # [Test]
        
    def read_file(self, file_name):
        with open(file=f'hw1/tasks/description/{file_name}') as f:
            return f.read()
    
if __name__ == '__main__':
    print('Hey')