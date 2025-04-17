class FileNumberProcessor:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def process_single_line(self, line, line_number):
        try:
            line = line.strip()
            num = int(line)
            print(f"成功处理数字:{num},平方:{num*num}")
        except ValueError:
            print(f"无效数据:第{line_number}行内容'{line}'不能转换为数字")
    
    def process_file(self, file_path): # file_path是单个文件的路径
        try:
            print(f'开始处理文件:{file_path}')
            with open(file_path, 'r', encoding = 'utf-8') as file:
                lines = file.readlines()
                line_number = 1
                for line in lines:
                    self.process_single_line(line, line_number)
                    line_number += 1
        except FileNotFoundError:
            print(f"文件{file_path}不存在")
        except PermissionError:
            print(f"无权限读取{file_path}")
        except Exception as e:
            print(f"处理文件{file_path}时发生未知错误:{e}")
        else:
            print(f"成功处理文件:{file_path}")
            
    def run(self):
        for file_path in self.file_paths:
            self.process_file(file_path)
            
if __name__ == "__main__":
    file_paths = ['/Users/wtsama/Documents/code/Wtever-repository/week7/numbers.txt', '/Users/wtsama/Documents/code/Wtever-repository/week7/another.txt']
    processor = FileNumberProcessor(file_paths)
    processor.run()
