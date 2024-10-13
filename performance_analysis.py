import tkinter as tk
from tkinter import ttk
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# MySQL connection settings
username = 'root'
password = 'Navee@03'
host = 'local host'
database = 'students'

# Connect to MySQL database
cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    database=database
)

# Create a Tkinter GUI window
root = tk.Tk()
root.title("Students' Academic Performance Analysis")

# Create a frame for the GUI elements
frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill="both", expand=True)

# Create a label and entry field for student ID
ttk.Label(frame, text="Student ID:").grid(column=0, row=0, sticky="W")
student_id_entry = ttk.Entry(frame, width=20)
student_id_entry.grid(column=1, row=0, sticky="W")

# Create a button to retrieve student data
def retrieve_student_data():
    student_id = student_id_entry.get()
    cursor = cnx.cursor()
    query = "SELECT * FROM students WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    student_data = cursor.fetchone()
    if student_data:
        display_student_data(student_data)
    else:
        print("Student not found")

ttk.Button(frame, text="Retrieve Student Data", command=retrieve_student_data).grid(column=2, row=0, sticky="W")

# Create a label and text box to display student data
ttk.Label(frame, text="Student Data:").grid(column=0, row=1, sticky="W")
student_data_text = tk.Text(frame, width=40, height=10)
student_data_text.grid(column=1, row=1, sticky="W")

# Create a button to analyze student performance
def analyze_student_performance():
    student_id = student_id_entry.get()
    cursor = cnx.cursor()
    query = "SELECT * FROM student_performance WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    performance_data = cursor.fetchall()
    if performance_data:
        analyze_performance_data(performance_data)
    else:
        print("No performance data found")

ttk.Button(frame, text="Analyze Student Performance", command=analyze_student_performance).grid(column=2, row=1, sticky="W")

# Create a label and text box to display analysis results
ttk.Label(frame, text="Analysis Results:").grid(column=0, row=2, sticky="W")
analysis_results_text = tk.Text(frame, width=40, height=10)
analysis_results_text.grid(column=1, row=2, sticky="W")

# Function to display student data
def display_student_data(student_data):
    student_data_text.delete(1.0, "end")
    student_data_text.insert("end", "Student ID: {}\n".format(student_data[0]))
    student_data_text.insert("end", "Name: {}\n".format(student_data[1]))
    student_data_text.insert("end", "Gender: {}\n".format(student_data[2]))
    student_data_text.insert("end", "Age: {}\n".format(student_data[3]))
    student_data_text.insert("end", "Grade Level: {}\n".format(student_data[4]))

# Function to analyze performance data
def analyze_performance_data(performance_data):
    analysis_results_text.delete(1.0, "end")
    df = pd.DataFrame(performance_data, columns=["Student ID", "Math Score", "Science Score", "English Score"])
    analysis_results_text.insert("end", "Descriptive Statistics:\n")
    analysis_results_text.insert("end", df.describe().to_string())
    analysis_results_text.insert("end", "\n\nVisualizations:\n")
    plt.hist(df["Math Score"], bins=10)
    plt.xlabel("Math Score")
    plt.ylabel("Frequency")
    plt.title("Distribution of Math Scores")
    plt.show()
    sns.scatterplot(x="Math Score", y="Science Score", data=df)
    plt.xlabel("Math Score")
    plt.ylabel("Science Score")
    plt.title("Relationship between Math and Science Scores")
    plt.show()

# Start the Tkinter GUI event loop
root.mainloop()
