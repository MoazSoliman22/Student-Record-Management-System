import streamlit as st
import pandas as pd
import os
import csv
from sklearn.linear_model import LinearRegression
import numpy as np

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.grades = []

    def add_grade(self, subject, score, credits, study_hours):
        self.grades.append({
            'Subject': subject,
            'Score': score,
            'Credits': credits,
            'StudyHours': study_hours
        })

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        for grade in self.grades:
            points = self.get_grade_points(grade['Score'])
            total_points += points * grade['Credits']
            total_credits += grade['Credits']
        
        return 0.0 if total_credits == 0 else total_points / total_credits

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

class StudentSystem:
    def __init__(self):
        self.students = {}
        self.filename = 'student_records.csv'
        self.load_data()

    def add_student(self, id, name):
        if id in self.students:
            return False
        self.students[id] = Student(id, name)
        self.save_data()
        return True

    def add_grade(self, id, subject, score, credits, study_hours):
        if id in self.students:
            self.students[id].add_grade(subject, score, credits, study_hours)
            self.save_data()
            return True
        return False

    def save_data(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Subject', 'Score', 'Credits', 'StudyHours'])
            for s in self.students.values():
                if not s.grades:
                    writer.writerow([s.id, s.name, '', '', '', ''])
                else:
                    for g in s.grades:
                        writer.writerow([s.id, s.name, g['Subject'], g['Score'], g['Credits'], g.get('StudyHours', 0)])

    def load_data(self):
        if not os.path.exists(self.filename): return
        try:
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        uid = int(row['ID'])
                        if uid not in self.students:
                            self.students[uid] = Student(uid, row['Name'])
                        
                        if row['Subject']:
                            self.students[uid].add_grade(
                                row['Subject'], 
                                float(row['Score']), 
                                float(row['Credits']),
                                float(row['StudyHours']) if row.get('StudyHours') else 0.0
                            )
                    except ValueError: continue
        except Exception: pass

    def get_all_ids(self):
        return list(self.students.keys())

    def get_student_name(self, uid):
        return self.students[uid].name if uid in self.students else "Unknown"


# STREAMLIT UI (The "Frontend")
st.set_page_config(page_title="Student Manager", page_icon="🎓", layout="centered")
st.title("Student Record Management System")

if 'system' not in st.session_state:
    st.session_state.system = StudentSystem()

system = st.session_state.system

system.load_data()

tab1, tab2, tab3, tab4 = st.tabs(["Add Student", "Add Grade", "View Records", "AI Predictor"])

with tab1:
    st.header("Register New Student")
    col1, col2 = st.columns(2)
    with col1:
        new_id = st.number_input("Student ID", min_value=1, step=1)
    with col2:
        new_name = st.text_input("Full Name")
    
    if st.button("Save Student", type="primary"):
        if new_name:
            if system.add_student(new_id, new_name):
                st.success(f"Student '{new_name}' added successfully!")
            else:
                st.error(f"Error: ID {new_id} already exists.")
        else:
            st.warning("Please enter a name.")

with tab2:
    st.header("Log Academic Performance")
    all_ids = system.get_all_ids()
    if not all_ids:
        st.info("No students found. Please add a student first.")
    else:
        selected_id = st.selectbox("Select Student ID", all_ids, format_func=lambda x: f"{x} - {system.get_student_name(x)}")
        
        c1, c2 = st.columns(2)
        with c1:
            subject = st.text_input("Subject Name")
            credits = st.number_input("Credits", min_value=1, value=3)
        with c2:
            score = st.number_input("Score (0-100)", min_value=0, max_value=100)
            hours = st.number_input("Hours Studied", min_value=0.0, step=0.5)

        if st.button("Add Grade"):
            if subject:
                system.add_grade(selected_id, subject, score, credits, hours)
                st.success(f"Grade for {subject} added!")
            else:
                st.warning("Please enter a subject name.")

with tab3:
    st.header("Student Records")
    
    if os.path.exists(system.filename):
        df = pd.read_csv(system.filename)
        st.subheader("GPA Report")
        for uid, student in system.students.items():
            gpa = student.calculate_gpa()
            with st.expander(f"{student.name} (ID: {uid}) - GPA: {gpa:.2f}"):
                if not student.grades:
                    st.write("No grades recorded.")
                else:
                    student_grades = pd.DataFrame(student.grades)
                    st.table(student_grades[['Subject', 'Score', 'Credits']])
    else:
        st.info("No records found.")

with tab4:
    st.header("AI Score Predictor")
    st.write("This model uses **Linear Regression** to predict your score based on study hours.")

    if os.path.exists(system.filename):
        df = pd.read_csv(system.filename)
        df_clean = df.dropna(subset=['Score', 'StudyHours'])
        
        if len(df_clean) < 5:
            st.warning(f"Not enough data to train the AI. (Current records: {len(df_clean)}/5 needed)")
        else:
            X = df_clean[['StudyHours']]
            y = df_clean['Score']
            model = LinearRegression()
            model.fit(X, y)

            study_input = st.slider("How many hours do you plan to study?", 0, 20, 5)
            
            if st.button("Predict My Score"):
                prediction = model.predict([[study_input]])
                predicted_score = min(100, max(0, prediction[0]))
                
                st.balloons()
                st.success(f"Predicted Score: **{predicted_score:.2f}**")
                

                st.subheader("Study Hours vs. Score Trend")
                chart_data = df_clean[['StudyHours', 'Score']]
                st.scatter_chart(chart_data, x='StudyHours', y='Score')
    else:
        st.error("No database found.")