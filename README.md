# Student-Record-Management-System
A command-line application designed to track student academic performance, calculate weighted GPAs, and predict future grades using Machine Learning.

## Key Features
* **Student Management:** Create and manage student profiles with unique IDs.
* **Grade Tracking:** Record grades with support for:
    * Subject Name
    * Score (0-100)
    * Credit Hours (Weighted GPA)
    * Study Hours (For AI Training)
* **Weighted GPA Calculation:** Automatically converts scores to a 4.0 scale and calculates GPA based on credit weights.
* **Data Persistence:** All data is automatically saved to `student_records.csv`, ensuring no data is lost between sessions.
* AI Score Predictor: Uses **Linear Regression** (`scikit-learn`) to analyze past study habits and predict future exam scores.

## Installation & Setup
### Clone the Repository
```bash
git clone [https://github.com/MoazSoliman22/Student-Record-Management-System.git](https://github.com/MoazSoliman22/Student-Record-Management-System.git)
cd Student-Record-Management-System
