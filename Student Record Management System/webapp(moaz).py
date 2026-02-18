import os
import csv
import streamlit as st

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.grades = []

    def __str__(self):
        return f'Student ID: {self.id}\nStudent name: {self.name}'

    def add_grade(self, subject, score, credits):
            self.grades.append({
                'Subject' : subject,
                'Score' : score,
                'Credits' : credits
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
        if score >= 93:
            return 4.0
        elif score >= 90:
            return 3.7
        elif score >= 87:
            return 3.3
        elif score >= 83:
            return 3.0
        elif score >= 80:
            return 2.7
        elif score >= 77:
            return 2.3
        elif score >= 73:
            return 2.0
        elif score >= 70:
            return 1.7
        elif score >= 67:
            return 1.3
        elif score >= 60:
            return 1.0
        else:
            return 0.0

    def get_letter_grade(self, score):
        if score >= 93:
            return 'A'
        elif score >= 90:
            return 'A-'
        elif score >= 87:
            return 'B+'
        elif score >= 83:
            return 'B'
        elif score >= 80:
            return 'B-'
        elif score >= 77:
            return 'C+'
        elif score >= 73:
            return 'C'
        elif score >= 70:
            return 'C-'
        elif score >= 67:
            return 'D+'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

class StudentSystem:
    def __init__(self):
        self.students = {}
        self.filename = 'student_records.csv'

    def add_student(self, student):
        if student.id in self.students:
            print(f'Student with Id {student.id} is already exist')
            return False
        else:
            self.students[student.id] = student
            return True

    def add_grade(self, id, subject, score, credits):
        if not self.search_by_id(id):
            return
        else:
            self.search_by_id(id).add_grade(subject, score, credits)

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
            fieldnames = ['ID', 'Name', 'Subject', 'Score', 'Credits']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

            for student in self.students.values():
                if not student.grades:
                    writer.writerow([student.id, student.name, '', '', ''])
                else:
                    for grade in student.grades:
                        student_data = [student.id, student.name, grade['Subject'], grade['Score'], grade['Credits']]
                        writer.writerow(student_data)
    
    def load_data(self):
        abs_path = os.path.abspath(self.filename)
        if not os.path.isfile(abs_path):
            print('File not found')
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
                            self.students[id].add_grade(subject, score, credits)
                    
                    except ValueError:
                        continue
    
    def view_records(self):
        for student in self.students.values():
            print(student)
            if not student.grades:
                print('No subjects yet')
            else:
                for student_grade in student.grades:
                    letter = student.get_letter_grade(student_grade['Score'])
                    print(f'{student_grade['Subject']} ({letter})')
            print('-'*20)


st.set_page_config(page_title='Student Manager', page_icon='🎓', layout= 'centered')
st.title('Student Record Management System')

if 'system' not in st.session_state:
    st.session_state.system = StudentSystem()
system = st.session_state.system

system.load_data()
tab1, tab2, tab3 = st.tabs(['Add Student', 'Add Grade', 'View Records'])

with tab1:
    st.header('Add Student')

    student_id = st.number_input('Student ID', min_value=1, step=1)
    student_name = st.text_input('Student Name')

    if st.button('Add Student'):
        if student_name:
            new_student = Student(student_id, student_name)
            if system.add_student(new_student):
                system.save_data()
                st.success('Student added successfully ✅')
            else:
                st.error('ID already exists ❌')
        else:
            st.error('Please enter a name')

with tab2:
    st.header('Add Grade')

    if not system.students:
        st.info('Not students yet.')
    else:
        selected_id = st.selectbox('Select Student', list(system.students.keys()))

        subject = st.text_input('Subject')
        score = st.number_input('Score', min_value=0, max_value=100)
        credits = st.number_input('Credits', min_value=1)

        if st.button('Add Grade'):
            if subject:
                system.add_grade(selected_id, subject, score, credits)
                system.save_data()
                st.success('Grade added successfully ✅')
            else:
                st.error('Enter subject name')

with tab3:
    st.header('View Records')

    if not system.students:
        st.info('No records yet')
    else:
        for student in system.students.values():
            gpa = student.calculate_gpa()

            with st.expander(f"{student.name} (ID: {student.id}) - GPA: {gpa:.2f}"):
                if not student.grades:
                    st.write('No subjects yet.')
                else:
                    for grade in student.grades:
                        letter = student.get_letter_grade(grade['Score'])

                        st.write(f"{grade['Subject']} - {grade['Score']} ({letter})")