class InvalidGradeError(Exception):
    def __init__(self, grade):
        self.grade = grade
        self.message = f"成绩无效:{grade}"
        super().__init__(self.message)

class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []
    def add_grade(self,grade):
        try:
            if not (0 <= grade <= 100):
                raise InvalidGradeError(grade) # 抛出异常
            self.grades.append(grade)
        except InvalidGradeError as e:
            print(e) # 捕获异常并打印信息
        
    def total_score(self):
        return sum(self.grades)
    def average_score(self):
        if len(self.grades)!=0:
            return sum(self.grades)/len(self.grades)
        else:
            return 0

if __name__ == "__main__":
    #输入学生姓名并且创建类实例student
    name = input()
    student = Student(name)
    #输入学生成绩
    grades = map(int, input().split())
    #添加成绩
    for grade in grades:
        student.add_grade(grade)
    print(f"总成绩:{student.total_score()},平均成绩:{student.average_score():.1f}")
    ###end