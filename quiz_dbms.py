import sqlite3
import random

# Connect to SQLite database
conn = sqlite3.connect("quiz_app_simple.db")
cursor = conn.cursor()

# Create tables for users and quiz questions
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    quizzes_taken INTEGER DEFAULT 0,
    last_score INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    answer TEXT NOT NULL
)
''')

conn.commit()

# Add questions to the database if empty
questions_data = {
    "Python": [
        ("What is the output of print(2 ** 3)?", "6,8,9,7", "8"),
        ("Which data type is immutable?", "List,Set,Dictionary,Tuple", "Tuple"),
        ("How do you create a function in Python?", "function(),def(),create(),lambda()", "def()"),
    ],
    "DSA": [
        ("What is the time complexity of binary search?", "O(n),O(log n),O(n^2),O(1)", "O(log n)"),
        ("Which data structure is FIFO?", "Stack,Queue,Tree,Graph", "Queue"),
        ("What does DFS stand for?", "Depth First Search,Data First Search,Dynamic First Search,Directed First Search", "Depth First Search"),
    ],
    "DBMS": [
        ("What does DBMS stand for?", "Data Base Management System,Database Management System,Data Backup Management System,Data Business Management System", "Database Management System"),
        ("Which SQL command is used to fetch data?", "FETCH,SELECT,GET,DISPLAY", "SELECT"),
        ("What is a primary key?", "Unique identifier,Any column,Foreign key,Redundant data", "Unique identifier"),
    ]
}

cursor.execute("SELECT COUNT(*) FROM quiz_questions")
if cursor.fetchone()[0] == 0:
    for topic, questions in questions_data.items():
        for question, options, answer in questions:
            cursor.execute("INSERT INTO quiz_questions (topic, question, options, answer) VALUES (?, ?, ?, ?)",
                        (topic, question, options, answer))
    conn.commit()

# Functions
def register():
    username = input("Enter a username: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username already exists. Try logging in.")
        return
    password = input("Enter a password: ")
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("Registration successful!")

def login():
    username = input("Enter your username: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        print("Username not found. Please register first.")
        return None
    password = input("Enter your password: ")
    if user[1] == password:
        print("Login successful!")
        return username
    else:
        print("Incorrect password.")
        return None

def take_quiz(username):
    print("Starting the quiz...")
    score = 0
    topics = ["Python", "DSA", "DBMS"]
    random.shuffle(topics)

    for topic in topics:
        print(f"Topic: {topic}")
        cursor.execute("SELECT * FROM quiz_questions WHERE topic = ? ORDER BY RANDOM() LIMIT 5", (topic,))
        questions = cursor.fetchall()
        for q in questions:
            print(f"{q[2]}")
            options = q[3].split(',')
            for i, option in enumerate(options, start=1):
                print(f"{i}. {option}")
            answer = input("Enter your answer (1-4): ")
            if options[int(answer) - 1] == q[4]:
                score += 1
                print("Correct!")
            else:
                print(f"Wrong! The correct answer is: {q[4]}")

    cursor.execute("UPDATE users SET quizzes_taken = quizzes_taken + 1, last_score = ? WHERE username = ?", (score, username))
    conn.commit()
    print(f"Quiz completed! Your score is {score}/15.")

def view_profile(username):
    cursor.execute("SELECT quizzes_taken, last_score FROM users WHERE username = ?", (username,))
    profile = cursor.fetchone()
    print("Your Profile:")
    print(f"Quizzes Taken: {profile[0]}")
    print(f"Last Score: {profile[1]}")

# Main Program
def main():
    while True:
        print("Welcome to the Quiz App!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                while True:
                    print("1. Take Quiz")
                    print("2. View Profile")
                    print("3. Logout")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == "1":
                        take_quiz(username)
                    elif sub_choice == "2":
                        view_profile(username)
                    elif sub_choice == "3":
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
main()

# Close the database connection
conn.close()
