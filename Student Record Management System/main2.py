import os
import csv
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.grades = []

    def __str__(self):
        return f'Student ID: {self.id}\nStudent name: {self.name}'

    def add_grade(self, subject, score, credits, study_hours):
            self.grades.append({
                'Subject' : subject,
                'Score' : score,
                'Credits' : credits,
                'StudyHours': study_hours
            })
    
    def calculate_gpa(self):
        total_points = 0
        total_credits = 0

        for grade in self.grades:
            grade_point = self.get_grade_points(grade['Score'])
            total_points += grade_point * grade['Credits']
            total_credits += grade['Credits']

        if total_credits == 0:
            return 0.0
        else:
            gpa = total_points / total_credits
            return gpa

    def get_grade_points(self, score):
        if score >= 93: return 4.0
        elif score >= 90: return 3.7
        elif score >= 87: return 3.3
        elif score >= 83: return 3.0
        elif score >= 80: return 2.7
        elif score >= 77: return 2.3
        elif score >= 73: return 2.0
        elif score >= 70: return 1.7
        elif score >= 67: return 1.3
        elif score >= 60: return 1.0
        else: return 0.0

    def get_letter_grade(self, score):
        if score >= 93: return 'A'
        elif score >= 90: return 'A-'
        elif score >= 87: return 'B+'
        elif score >= 83: return 'B'
        elif score >= 80: return 'B-'
        elif score >= 77: return 'C+'
        elif score >= 73: return 'C'
        elif score >= 70: return 'C-'
        elif score >= 67: return 'D+'
        elif score >= 60: return 'D'
        else: return 'F'

class StudentSystem:
    def __init__(self):
        self.students = {}
        self.filename = 'student_records.csv'

    def add_student(self, student):
        if student.id in self.students:
            print(f'Error: Student with Id {student.id} already exists')
            return False
        else:
            self.students[student.id] = student
            return True

    def add_grade(self, id, subject, score, credits, study_hours):
        if not self.search_by_id(id):
            return
        else:
            self.search_by_id(id).add_grade(subject, score, credits, study_hours)

    def get_student_info(self):
        while True:
            try:
                student_id = int(input('Enter your Id\n-> '))
                if not student_id > 0:
                    raise ValueError
                break
            except ValueError:
                print("Id must be a number")
        
        while True:
            try:
                student_name = input('Enter your name\n-> ').lower().strip()
                if not student_name.replace(" ","").isalpha():
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. (Only letters)")
        
        return student_id, student_name
    
    def search_by_id(self, id):
        if id not in self.students.keys():
            return None
        else:
            return self.students[id]

    def get_id(self):
        while True:
            try:
                id = int(input('Enter your id\n-> '))
                if id <= 0 :
                    raise ValueError
                break
            except ValueError:
                print('please enter an integer')
        
        if not id in self.students:
            return None
        return id

    def save_data(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Name', 'Subject', 'Score', 'Credits', 'StudyHours']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

            for student in self.students.values():
                if not student.grades:
                     writer.writerow([student.id, student.name, '', '', '', ''])
                else:
                    for grade in student.grades:
                        student_data = [
                            student.id, 
                            student.name, 
                            grade['Subject'], 
                            grade['Score'], 
                            grade['Credits'],
                            grade.get('StudyHours', 0)
                        ]
                        writer.writerow(student_data)
    
    def load_data(self):
        abs_path = os.path.abspath(self.filename)
        if not os.path.isfile(abs_path):
            print('File not found. Starting fresh.')
        else:
            with open(abs_path,'r' ,newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        id = int(row['ID'])
                        name = row['Name']
                        
                        if id not in self.students:
                            self.students[id] = Student(id, name)
                        
                        if row['Subject']:
                            subject = row['Subject']
                            score = float(row['Score'])
                            credits = float(row['Credits'])
                            study_hours = float(row['StudyHours']) if 'StudyHours' in row and row['StudyHours'] else 0.0
                            
                            self.students[id].add_grade(subject, score, credits, study_hours)
                    except ValueError:
                        continue
    
    def view_records(self):
        print("\n--- Student Records ---")
        for student in self.students.values():
            print(student)
            gpa = student.calculate_gpa()
            print(f"Overall GPA: {gpa:.2f}")
            
            if not student.grades:
                print('No subjects yet')
            else:
                for student_grade in student.grades:
                    letter = student.get_letter_grade(student_grade['Score'])
                    print(f"  - {student_grade['Subject']}: {student_grade['Score']} ({letter}) | Study Hours: {student_grade['StudyHours']}")
            print('-'*20)

    def predict_score(self):
        print("\n--- AI Score Predictor ---")
        try:
            df = pd.read_csv(self.filename)
        except FileNotFoundError:
            print("No data found.")
            return

        if 'StudyHours' not in df.columns:
            print("Error: Your data file is old. Please add new grades with 'Study Hours' first.")
            return
        
        df = df.dropna(subset=['Score', 'StudyHours'])
        
        if len(df) < 5:
            print(f"Not enough data to train AI. You have {len(df)} records, but need at least 5.")
            return

        X = df[['StudyHours']]
        y = df['Score']
        
        model = LinearRegression()
        model.fit(X, y)

        try:
            hours = float(input("How many hours do you plan to study?\n-> "))
            prediction = model.predict([[hours]])
            print(f"Based on history, if you study {hours} hours, you might score: {prediction[0]:.2f}")
        except ValueError:
            print("Invalid input.")

def main():
    system = StudentSystem()
    system.load_data()
    
    while True:
        menu = '\n1) Add Student\n2) Add Grade\n3) Calculate GPA (one student)\n4) View Records\n5) Predict Score (Phase 3)\n0) Exit'
        print(menu)
        while True:
            try:
                choice = input('Make a decision-> ').strip()
                if not choice.isdigit():
                    raise ValueError
                break
            except ValueError:
                    print('Please enter a number (0-5)')

        if choice == '1':
            id, name = system.get_student_info() 
            student = Student(id, name)
            if system.add_student(student):
                system.save_data()
                print(f"Student {name} added.")
        
        elif choice == '2':
            student_id = system.get_id()
            if not student_id:
                print(f'Student not found')
            else:
                while True:
                    try:
                        subject_num = int(input('How many subjects\n-> '))
                        if subject_num <= 0:
                            raise ValueError
                        break
                    except ValueError:
                        print('Please enter a number')
                
                for num in range(subject_num):
                    print(f'----Subject number ({num + 1})----')
                    student_subject = input('Subject name\n-> ').title()
                    
                    while True:
                        try:
                            student_score = int(input('Score (0-100)\n-> '))
                            if not 0 <= student_score <= 100:
                                raise ValueError
                            break
                        except ValueError:
                            print('Score must be an integer between 0 and 100')
                    
                    while True:
                        try:
                            student_credits = int(input('Credits\n-> '))
                            if student_credits <= 0:
                                raise ValueError
                            break
                        except:
                            print('Invalid input. credit cannot be zero')
                    
                    while True:
                        try:
                            study_hours = float(input('Hours Studied\n-> '))
                            if study_hours < 0: raise ValueError
                            break
                        except:
                            print('Invalid input.')

                    system.add_grade(student_id, student_subject, student_score, student_credits, study_hours)
                    system.save_data()
                    print(f"Grade for {student_subject} saved.")
        
        elif choice == '3':
            student_id = system.get_id()
            if not student_id:
                print('Student not found')
            else:
                student_search = system.search_by_id(student_id)
                gpa = student_search.calculate_gpa()
                print(f'GPA = {gpa:.2f}')
        
        elif choice == '4':
            system.view_records()
        
        elif choice == '5':
            system.predict_score()
            
        elif choice == '0':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()